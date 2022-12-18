import os
from dataclasses import asdict, dataclass, field
from typing import List

import yaml


@dataclass
class BotArg:
    name: str
    description: str
    type: int


@dataclass
class BotCommand:
    name: str
    description: str
    type: int
    id: str = ""
    arguements: List[BotArg] = field(default_factory=lambda: [])


@dataclass
class BotInfo:
    name: str
    app_id: str
    interaction_url: str
    secrets_arn: str = None
    hosted_zone_id: str = None
    commands: List[BotCommand] = field(default_factory=lambda: [])

    def crupdate_info_file(self, file_path: str):
        with open(file_path, "w") as f:
            f.write(yaml.safe_dump(asdict(self), sort_keys=False))

    @staticmethod
    def load_from_file(file_path: str):
        try:
            with open(file_path) as f:
                data = f.read()
        except:
            raise Exception(f"Could not read file {file_path}")

        parsed_data = yaml.safe_load(data)
        parsed_data["commands"] = list(
            map(lambda x: BotCommand(**x), parsed_data.get("commands", []))
        )
        return BotInfo(**parsed_data)

    @staticmethod
    def get_default_path():
        return f"{os.getcwd()}/bot_info.yml"
