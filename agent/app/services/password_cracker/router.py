from fastapi import APIRouter, HTTPException
from app.services.password_cracker.manager import crack_range

router = APIRouter()


@router.post("/")
async def crack(payload: dict):
    try:
        target_hash = payload["hash"]
        range_start = int(payload["range_start"])
        range_end = int(payload["range_end"])
    except (KeyError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Invalid payload. Expecting keys: hash, range_start, range_end",
        )

    result = await crack_range(target_hash, range_start, range_end)
    if result:
        print(f"Found matching phone number: {result}")
        return {
            "found": True,
            "range_start": range_start,
            "range_end": range_end,
            "phone_number": result,
        }
    else:
        return {"found": False}
