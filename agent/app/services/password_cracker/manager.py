import hashlib
from .utils import format_phone


async def crack_range(target_hash: str, range_start: int, range_end: int) -> str:
    for num in range(range_start, range_end):
        phone_number = format_phone(num)
        computed_hash = hashlib.md5(phone_number.encode("utf-8")).hexdigest()
        if computed_hash == target_hash:
            return phone_number
    return ""
