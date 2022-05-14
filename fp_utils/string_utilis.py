import random
import string


def random_string(
    size: int = 10, chars=string.ascii_uppercase + string.digits
) -> str:
    return ''.join(random.choice(chars) for _ in range(size))