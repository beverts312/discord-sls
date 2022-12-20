import logging

from discord_sls.cli.models import BotInfo


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
    interaction_url = input("Interaction URL: ")
    bot_info = BotInfo(
        name=name, app_id=app_id, interaction_url=interaction_url
    )
    bot_info.crupdate_info_file(kwargs.get("config"))
    logging.info("Created bot_info.yml")
