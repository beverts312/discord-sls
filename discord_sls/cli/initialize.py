import json
import logging

import boto3
import requests

from discord_sls.cli.models import BotInfo

TEMPLATE_URL = "https://raw.githubusercontent.com/beverts312/discord-bot-template/3d2021606b26e0188a320d6c110fc896774bfa6b/template.yml"
SAMCONFIG_TEMPLATE = """
version = 0.1
[default]
[default.deploy]
[default.deploy.parameters]
stack_name = "{name}"
s3_bucket = "{sam_bucket}"
s3_prefix = "{name}"
region = "{region}"
capabilities = "CAPABILITY_IAM"
parameter_overrides = "Stage=\\"dev\\" Domain=\\"{domain}\\" HostedZoneId=\\"{hosted_zone_id}\\" BotSecretArn=\\"{secrets_arn}\\" BotName=\\"{name}\\""
image_repositories = []
"""


def setup_secret(bot_name, discord_public_key):
    client = boto3.client("secretsmanager", region_name="us-east-1")
    response = client.create_secret(
        Name=f"{bot_name}-secrets",
        SecretString=json.dumps({"discord_public_key": discord_public_key}),
        ForceOverwriteReplicaSecret=True,
    )
    return response["ARN"]


def create_sam_files(
    bot_dir: str,
    name: str,
    domain: str,
    hosted_zone_id: str,
    secrets_arn: str,
    sam_bucket: str,
):
    logging.info("Downloading SAM Template")
    res = requests.get(TEMPLATE_URL)
    with open(f"{bot_dir}/template.yml", "w") as f:
        f.write(res.text)
    logging.info("Creating samconfig.toml")
    with open(f"{bot_dir}/samconfig.toml", "w") as f:
        f.write(
            SAMCONFIG_TEMPLATE.format(
                name=name,
                domain=domain,
                hosted_zone_id=hosted_zone_id,
                secrets_arn=secrets_arn,
                sam_bucket=sam_bucket,
                region="us-east-1",
            )
        )


def initialize_bot(**kwargs):
    logging.info(
        "If you have not yet created the bot in the discord developer portal do that now"
    )
    name = kwargs.get("name", input("Bot name: "))
    app_id = kwargs.get(
        "app_id",
        input(
            "Discord App ID (create at https://discord.com/developers/applications): "
        ),
    )
    setup_sam = input("Do you want to setup SAM? (Y/n): ")
    if setup_sam.lower() != "n":
        key = input("Discord Public Key: ")
        secrets_arn = setup_secret(name, key)
        logging.info(f"Created secret {secrets_arn}")
        domain = input("Domain: ")
        hosted_zone_id = input("Hosted Zone ID: ")
        sam_bucket = input("SAM Template Bucket: ")
        create_sam_files(
            kwargs.get("config").replace("bot_info.yml", ""),
            name,
            domain,
            hosted_zone_id,
            secrets_arn,
            sam_bucket,
        )
        bot_info = BotInfo(
            app_id=app_id,
            name=name,
            interaction_url=f"https://{domain}/api/interactions",
            secrets_arn=secrets_arn,
            hosted_zone_id=hosted_zone_id,
            commands=[],
        )
    else:
        interaction_url = input("Interaction URL: ")
        bot_info = BotInfo(
            name=name, app_id=app_id, interaction_url=interaction_url
        )

    bot_info.crupdate_info_file(kwargs.get("config"))
    logging.info("Created bot_info.yml")
    logging.info(
        "After the bot is deployed, navigate to your app in the developer portal"
    )
    if bot_info.interaction_url:
        logging.info(
            f"Find the 'INTERACTIONS ENDPOINT URL' field and set it to: {bot_info.interaction_url}"
        )
    else:
        logging.info("Be sure to set the interaction url")
    logging.info(
        "When you click save discord will validate that your bot is working"
    )
