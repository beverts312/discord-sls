# Discord SLS

A set of tools for building a discord bot with a serverless architecture in mind. If you are looking for a more complete discord sdk, check out [discord.py](https://github.com/Rapptz/discord.py).

![PyPI](https://img.shields.io/pypi/v/discord_sls)

Install with pip: `pip install discord_sls`

[Example/Template Repo](https://github.com/beverts312/discord-bot-template)

## Usage

The library provides a decorator `@bot_handler` which can be used to decorate a lambda handler to respond to discord api requests.
It will handle the ping-pong handshake, and will parse the request body into a python object for you to use. The decorator expects you to return [Ineraction Callback Data](https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-response-object-interaction-callback-data-structure).

Discord expects a quick response to the initial request, if your bot needs longer to handle an interaction you can use the `send_command_to_queue` function to send the command to a queue for processing in another lambda (aditional decorator coming soon). The queue is determined by the `LONG_RESPONSE_QUEUE` environment variable.

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

### Keeping the bot warm

With most serverless architectures you will need to keep your lambdas warm to avoid cold start times. The `@bot_handler` decorator will automatically handle these requests for you.
If using the template provided by the cli, it will automatically provision a cloud watch event rule to keep your bot warm. If using your own template you will want to add something like this:

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

## Getting Started with the CLI

The package includes a cli which can make it easy for you to manage the lifecycle of your bot, and will provide infrastructure templates and configuration neccessary to run your bot.
The cli/templates are highly opinonated and aimed at providing simple gitops approach to mangaging the bot, you can use the pieces of it you like and leave the pieces of it you dont, you do not have to use the cli or the templates for the library to work for your application.

The `discord-sls init` command will create the following files:

- `bot_info.yml` - contains information about your bot, this will be used to help keep the config in discord and in your repo synced
- `template.yml` - an AWS SAM template that will provision the infrastructure needed to run your bot
- `samconfig.toml` - a config file for the AWS SAM cli

First ensure you have installed: python3, pip3, virtualenv, aws cli and the sam cli.
You will also need an AWS account and a Discord Developer account.
The existing template assumes you want to use a route53 hosted zone to manage your domain name. If you don't want to use this you will need to modify the template.

In your project directory, run `discord-sls init` and follow the prompts.
