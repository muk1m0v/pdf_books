from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    database_url: str | None
    ai_api_key: str | None
    admin_ids: tuple[int, ...]


def _parse_admin_ids(raw_ids: str | None) -> tuple[int, ...]:
    if not raw_ids:
        return ()

    admin_ids: list[int] = []
    for raw_id in raw_ids.split(","):
        raw_id = raw_id.strip()
        if raw_id:
            admin_ids.append(int(raw_id))
    return tuple(admin_ids)


def load_settings() -> Settings:
    token = getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is missing in .env")

    return Settings(
        bot_token=token,
        database_url=getenv("DATABASE_URL"),
        ai_api_key=getenv("AI_API_KEY"),
        admin_ids=_parse_admin_ids(getenv("ADMIN_IDS")),
    )
