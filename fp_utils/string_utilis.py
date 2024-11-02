import re
import random
import string
from datetime import datetime
from typing import Optional


def random_string(
    size: int = 10, chars=string.ascii_uppercase + string.digits
) -> str:
    return ''.join(random.choice(chars) for _ in range(size))


def string_to_int(data: Optional[str]) -> Optional[int]:
    if not data:
        return None
    # Use regex to find the first integer substring in the data
    match = re.search(r'-?\d+', data.replace(",", "").strip())
    # If an integer-like substring is found, convert it to an integer
    return int(match.group()) if match else None


def korean_string_to_int(data: Optional[str]) -> Optional[int]:
    if not data:
        return None

    # Define multipliers for Korean units
    units = {
        "억": 10**8,
        "천": 10**3,
        "만": 10**4,
        "백": 10**2
    }

    # Remove commas and extra spaces
    data = data.replace(",", "").strip()
    total = 0
    current_value = 0

    # Use regex to find patterns with optional numbers followed by units
    matches = re.findall(r'(\d+)(억|천|만|백)?', data)
    
    for num, unit in matches:
        num = int(num)
        
        if unit in units:
            # Multiply the number by the corresponding unit and add to the total
            current_value += num * units[unit]
        else:
            # If no unit is found, this is the final number part without a multiplier
            current_value += num

    total += current_value
    return total


def string_to_float(data: Optional[str]) -> Optional[float]:
    if not data:
        return None
    # Remove commas and any surrounding whitespace
    data = data.replace(",", "").strip()
    # Use regex to find the first float-like substring (including potential decimal points)
    match = re.search(r'-?\d+(\.\d+)?', data)
    # If a float-like substring is found, convert it to a float
    return float(match.group()) if match else None


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
