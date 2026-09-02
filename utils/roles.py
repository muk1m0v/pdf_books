from collections.abc import Iterable


def is_admin(telegram_id: int, admin_ids: Iterable[int]) -> bool:
    return telegram_id in set(admin_ids)
