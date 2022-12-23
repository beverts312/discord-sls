# Discord SLS

A set of tools for building a discord bot with a serverless architecture in mind. If you are looking for a more complete discord sdk, check out [discord.py](https://github.com/Rapptz/discord.py).

![PyPI](https://img.shields.io/pypi/v/discord_sls)

Install with pip: `pip install discord_sls`

[Example/Template Repo](https://github.com/beverts312/discord-bot-template)

## Usage

The library provides a decorator `@bot_handler` which can be used to decorate a lambda handler to respond to discord api requests.
It will handle the ping-pong handshake, and will parse the request body into a python object for you to use. The decorator expects you to return [Ineraction Callback Data](https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-callback-data-structure).

Discord expects a quick response to the initial request, if your bot needs longer to handle an interaction you can use the `send_command_to_queue` function to send the command to a queue for processing in another lambda decorated with `@deferred_response_handler`. The queue is determined by the `LONG_RESPONSE_QUEUE` environment variable.

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


@deferred_response_handler
def long_response_handler(interaction: Interaction):
  interaction.follow_up({"content": "Hello...async"})
```

### Keeping the bot warm

With most serverless architectures you will need to keep your lambdas warm to avoid cold start times. A popular mechanism for doing that is using cloudwatch event rules, the `@bot_handler` decorator will automatically handle these requests for you.T his is what a SAM template could look like for the rule:

```yml
BotKeepWarm:
  Type: AWS::Events::Rule
  Properties:
    Description: Keeps the bot lambda warm
    Name: !Sub 'keep-warm-${Stage}'
    ScheduleExpression: rate(5 minutes)
    Targets:
      - Id: KeepWarmDiscordBot
        Arn: !GetAtt DiscordBotFunction.Arn
```
