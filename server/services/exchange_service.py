import httpx
from fastapi import HTTPException, status

### --------------------------------------------------###

FRANKFURTER_URL = "https://api.frankfurter.dev/v2/rates"
REQUEST_TIMEOUT_SECONDS = 5

### --------------------------------------------------###

def get_rates(base: str, quotes: list[str]) -> tuple[dict[str, float], str]:
    params = {"base": base, "quotes": ",".join(quotes), "providers": "ecb"}

    try:
        response = httpx.get(FRANKFURTER_URL, params = params, timeout = REQUEST_TIMEOUT_SECONDS)

    except httpx.RequestError as e:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = "The exchange rate service is not available right now"
        ) from e

    if response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Unknown currency: {response.json().get('message', '')}"
        )

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = f"The exchange rate service answered with HTTP {response.status_code}"
        )

    rows = response.json()
    rates = {row["quote"]: row["rate"] for row in rows}
    rates_date = rows[0]["date"] if rows else ""

    return rates, rates_date