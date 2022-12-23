import logging

import requests

DISCORD_API_BASE = "https://discord.com/api/v10"


class Interaction:
    def __init__(self, command_body):
        self.command_body = command_body
        self._interaction_path = f"{DISCORD_API_BASE}/webhooks/{self.command_body['application_id']}/{self.command_body['token']}"
        self._original_path = f"{self._interaction_path}/messages/@original"

    def _handle_res(self, res):
        if res.status_code != 200:
            logging.error(
                f"Error handling {self.command_body['id']}, response code: {res.status_code}"
            )
            logging.error(res.text)
        else:
            logging.info(f"successfully handled: {self.command_body['id']}")

    @property
    def command_name(self):
        return self.command_body.get("data", {}).get("name", "")

    def edit(self, updated_content):
        self._handle_res(
            requests.patch(self._original_path, json=updated_content)
        )

    def delete(self):
        self._handle_res(requests.delete(self._original_path))

    def follow_up(self, content):
        self._handle_res(requests.post(self._interaction_path, json=content))
