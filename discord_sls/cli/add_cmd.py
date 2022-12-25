import logging

from discord_sls.app_client import COMMAND_TYPES, AppClient
from discord_sls.cli.models import BotCommand, BotInfo
from discord_sls.cli.utils import select_item


def add_bot_command(bot_info: BotInfo, token, **kwargs):
    client = AppClient(bot_info.app_id, token)
    name = kwargs.get("name", input("Command name: "))
    description = kwargs.get("description", input("Command Description: "))
    command_type = select_item(
        COMMAND_TYPES, "Command Type: ", "name", "value"
    )
    bot_info.commands.append(BotCommand(name, description, command_type))
    client.create_command(name, description, command_type)
    bot_info.crupdate_info_file(kwargs.get("config"))
    logging.info(f"Added {name} : {description}")
