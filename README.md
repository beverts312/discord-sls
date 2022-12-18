# Discord SLS

A set of tools for building a discord bot with a serverless architecture in mind. If you are looking for a more complete discord sdk, check out [discord.py](https://github.com/Rapptz/discord.py).


[Example/Template Repo](https://github.com/beverts312/discord-bot-template)


## Usage

### Example Usage
```py
import json
import logging
from discord_sls import Interaction, bot_handler

@bot_handler
def discord_bot(command_body, send_command_to_queue):
    command_name = command_body.get("data", {}).get("name")
    if command_name == "hello":
        return {"content": "Hello Moto"}
    elif command_name == "helloasync":
        send_command_to_queue(command_body)
        return {"content": "Hello..."}
    else:
        logging.warn(f"unhandled command: {command_name}")
        return {"content": "Unknown Command"}


def long_response_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])
        interaction = Interaction(body)
        interaction.edit_interaction({"content": "Hello...async"})
```