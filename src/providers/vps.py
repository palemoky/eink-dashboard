"""VPS data usage provider using 64clouds API.

Fetches VPS data usage percentage with caching.
"""

import logging

import httpx

from src.config import Config
from src.core import cached
from src.exceptions import ProviderError

logger = logging.getLogger(__name__)

VPS_API_URL = "https://api.64clouds.com/v1/getServiceInfo"


@cached(ttl=600)  # Cache for 10 minutes
async def get_vps_info(client: httpx.AsyncClient) -> int:
    """Fetch VPS data usage percentage.

    Args:
        client: Async HTTP client instance

    Returns:
        Data usage percentage (0-100)

    Raises:
        ProviderError: If API request fails
    """
    if not Config.VPS_API_KEY:
        logger.warning("VPS API key not configured")
        return 0

    url = VPS_API_URL
    params = {"veid": Config.VPS_API_KEY}

    try:
        res = await client.get(url, params=params, timeout=10.0)
        res.raise_for_status()
        data = res.json()

        if data.get("error") != 0:
            return 0

        return int((data["data_counter"] / data["plan_monthly_data"]) * 100)

    except httpx.HTTPError as e:
        logger.error(f"VPS API Error: {e}")
        raise ProviderError("vps", "Failed to fetch VPS info", e) from e
    except Exception as e:
        logger.error(f"VPS API Error: {e}")
        raise ProviderError("vps", "Unexpected error", e) from e
