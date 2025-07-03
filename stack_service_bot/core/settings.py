from environs import Env
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    admin_id: int
    admins: list
    dev_url: str
    prod_url: str


@dataclass
class Settings:
    bots: Bots



def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID"),
            admins=env.list("ADMINS", sep=","),
            dev_url=env.str("DEV_API_URL_PREFIX"),
            prod_url=env.str("PROD_API_URL_PREFIX")

        )
    )


settings = get_settings('input')