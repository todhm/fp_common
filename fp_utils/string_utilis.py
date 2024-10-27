import random
import string
from datetime import datetime
from typing import Optional


def random_string(
    size: int = 10, chars=string.ascii_uppercase + string.digits
) -> str:
    return ''.join(random.choice(chars) for _ in range(size))


def string_to_int(
    data: Optional[str]
) -> Optional[int]:
    if not data:
        return None
    data = data.replace(",", '').strip()
    if data:
        return int(data)
    return None


def string_to_float(
    data: Optional[str]
) -> Optional[int]:
    if not data:
        return None
    data = data.replace(",", '').strip()
    if data:
        return float(data)
    return None


def date_string_to_age(
    age: str,
    dformat: str = "%Y-%m-%d"
) -> int:
    return (
        datetime.today().year -
        datetime.strptime(age, dformat).year
    ) - (
        (
            datetime.today().month, datetime.today().day
        ) < (
            datetime.strptime(age, dformat).month,
            datetime.strptime(age, dformat).day
        )
    )
