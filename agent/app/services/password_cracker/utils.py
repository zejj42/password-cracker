def format_phone(num: int) -> str:
    phone = f"05{num:08d}"
    return phone[:3] + "-" + phone[3:]
