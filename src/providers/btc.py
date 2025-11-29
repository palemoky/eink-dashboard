"""Bitcoin price data provider using CoinGecko API.

Fetches BTC price and 24-hour change with caching and retry logic.
"""

import logging

import httpx

from src.core import api_retry, cached
from src.exceptions import ProviderError

logger = logging.getLogger(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


@cached(ttl=180)  # Cache for 3 minutes
@api_retry
async def get_btc_data(client: httpx.AsyncClient) -> dict[str, float | str]:
    """Fetch Bitcoin price and 24-hour change from CoinGecko API.

    Args:
        client: Async HTTP client instance

    Returns:
        Dictionary containing USD price and 24h change percentage

    Raises:
        ProviderError: If API request fails
    """
    url = COINGECKO_URL
    params = {"ids": "bitcoin", "vs_currencies": "usd", "include_24hr_change": "true"}

    try:
        res = await client.get(url, params=params, timeout=10.0)
        if res.status_code == 200:
            return res.json().get("bitcoin", {"usd": 0, "usd_24h_change": 0})
    except httpx.HTTPError as e:
        logger.error(f"BTC API Error: {e}")
        raise ProviderError("btc", "Failed to fetch BTC price", e) from e
    except Exception as e:
        logger.error(f"BTC API Error: {e}")
        raise ProviderError("btc", "Unexpected error", e) from e

    return {"usd": "---", "usd_24h_change": 0}
