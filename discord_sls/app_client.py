import logging

import requests

COMMAND_TYPES = [
    {"name": "CHAT_INPUT", "value": 1},
    {"name": "USER", "value": 2},
    {"name": "MESSAGE", "value": 3},
]

COMMAND_OPTION_TYPES = [
    {"name": "SUB_COMMAND", "value": 1},
    {"name": "SUB_COMMAND_GROUP", "value": 2},
    {"name": "STRING", "value": 3},
    {"name": "INTEGER", "value": 4},
    {"name": "BOOLEAN", "value": 5},
    {"name": "USER", "value": 6},
    {"name": "CHANNEL", "value": 7},
    {"name": "ROLE", "value": 8},
    {"name": "MENTIONABLE", "value": 9},
    {"name": "NUMBER", "value": 10},
    {"name": "ATTACHMENT", "value": 11},
]
DISCORD_BASE_URL = "https://discord.com/api/v10"


class AppClient:
    def __init__(self, app_id, token):
        self.app_id = app_id
        self.headers = {
            "Authorization": f"Bot {token}",
        }

    def _make_request(self, method, path, req_args={}):
        res = method(
            f"{DISCORD_BASE_URL}/{path}", headers=self.headers, **req_args
        )
        if res.status_code > 299:
            logging.error(f"Request Failure to: {path}")
            logging.error(res.text)
            raise Exception(res.text)
        return res.json()

    def list_commands(self):
        return self._make_request(
            requests.get,
            f"applications/{self.app_id}/commands",
        )

    def create_command(self, name, description, command_type):
        return self._make_request(
            requests.post,
            f"applications/{self.app_id}/commands",
            {
                "json": {
                    "name": name,
                    "description": description,
                    "type": command_type,
                }
            },
        )
