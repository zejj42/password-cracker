import httpx

TIMEOUT_SECONDS = 30


async def fetch(
    url: str, method: str = "GET", json: dict = None, timeout: int = TIMEOUT_SECONDS
):
    method = method.upper()
    try:
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, timeout=timeout)
            elif method == "POST":
                response = await client.post(url, json=json, timeout=timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"Error while fetching {url} with method {method}: {e}")
        return None
