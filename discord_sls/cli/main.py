import logging
from argparse import ArgumentParser

from discord_sls.cli.initialize import initialize_bot
from discord_sls.cli.models import BotInfo


def main():
    parser = ArgumentParser(description="For building serverless discord bots")
    parser.add_argument("command", choices=["init", "info"])
    parser.add_argument(
        "--config",
        help="Path to bot_info.yml",
        default=BotInfo.get_default_path(),
    )

    init_parser = ArgumentParser(
        description="Initialize a new bot (interactive flow)", add_help=False
    )
    init_parser.add_argument("--name", help="Name of the bot", required=True)
    init_parser.add_argument("--app-id", help="Discord App ID", required=True)

    info_parser = ArgumentParser(
        description="Get info about a bot", add_help=False
    )

    subparsers = parser.add_subparsers()
    subparsers.add_parser("init", parents=[init_parser])
    subparsers.add_parser("info", parents=[info_parser])

    args = parser.parse_args()

    try:
        bot_info = BotInfo.load_from_file(args.config)
    except:
        if args.command != "init":
            logging.error(f"No existing bot info found at {args.config}")
            logging.error(
                "Please run 'discord-sls init' or specify the path to an existing file"
            )
            exit(1)

    if args.command == "info":
        print(bot_info)
    elif args.command == "init":
        initialize_bot(**vars(args))
    else:
        print(f"{args.command} comming soon")
