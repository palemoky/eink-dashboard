"""Data fetcher for retrieving display data based on mode.

This module handles data fetching logic for different display modes.
"""

import logging
from typing import Any

from src.providers import Dashboard

logger = logging.getLogger(__name__)


class DataFetcher:
    """Fetches data for different display modes.

    Responsibilities:
    - Route data fetching based on display mode
    - Handle mode-specific data requirements
    - Coordinate with Dashboard provider

    Example:
        >>> fetcher = DataFetcher(dashboard)
        >>> data = await fetcher.fetch("dashboard")
    """

    def __init__(self, dashboard: Dashboard):
        """Initialize data fetcher.

        Args:
            dashboard: Dashboard provider instance
        """
        self.dashboard = dashboard

    async def fetch(self, mode: str) -> dict[str, Any]:
        """Fetch data for a display mode.

        Args:
            mode: Display mode name

        Returns:
            Dictionary containing mode-specific data
        """
        logger.debug(f"Fetching data for mode: {mode}")

        if mode == "dashboard":
            return await self._fetch_dashboard()
        elif mode == "quote":
            return await self._fetch_quote()
        elif mode == "poetry":
            return await self._fetch_poetry()
        elif mode == "wallpaper":
            return await self._fetch_wallpaper()
        elif mode == "holiday":
            return await self._fetch_holiday()
        elif mode == "year_end":
            return await self._fetch_year_end()
        else:
            logger.warning(f"Unknown mode '{mode}', using dashboard")
            return await self._fetch_dashboard()

    async def _fetch_dashboard(self) -> dict[str, Any]:
        """Fetch dashboard data."""
        return await self.dashboard.fetch_dashboard_data()

    async def _fetch_quote(self) -> dict[str, Any]:
        """Fetch quote data."""
        from src.providers.quote import get_quote

        quote = await get_quote(self.dashboard.client)
        return {"quote": quote}

    async def _fetch_poetry(self) -> dict[str, Any]:
        """Fetch poetry data."""
        from src.providers.poetry import get_poetry

        poetry = await get_poetry(self.dashboard.client)
        return {"poetry": poetry}

    async def _fetch_wallpaper(self) -> dict[str, Any]:
        """Fetch wallpaper data (no data needed)."""
        return {}

    async def _fetch_holiday(self) -> dict[str, Any]:
        """Fetch holiday data."""
        from src.layouts.holiday import HolidayManager

        holiday_manager = HolidayManager()
        holiday = holiday_manager.get_holiday()
        return {"holiday": holiday}

    async def _fetch_year_end(self) -> dict[str, Any]:
        """Fetch year-end summary data."""
        return await self.dashboard.fetch_year_end_data()
