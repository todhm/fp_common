import random
import string
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
