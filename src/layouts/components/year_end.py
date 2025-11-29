"""Year-end summary component for dashboard layout."""

import datetime
import logging
from typing import Any

from PIL import ImageDraw

from ...renderer.dashboard import DashboardRenderer

logger = logging.getLogger(__name__)


class YearEndSummaryComponent:
    """Handles rendering of the year-end summary screen."""

    def __init__(self, renderer: DashboardRenderer):
        self.renderer = renderer

    def draw(
        self, draw: ImageDraw.ImageDraw, width: int, height: int, summary_data: dict[str, Any]
    ) -> None:
        """Draw year-end summary (displayed on Dec 31st).

        Args:
            draw: PIL ImageDraw object
            width: Canvas width
            height: Canvas height
            summary_data: Year-end summary statistics
        """
        r = self.renderer
        now = datetime.datetime.now()
        year = now.year

        # Title
        title = f"{year} GitHub Summary"
        r.draw_centered_text(
            draw,
            width // 2,
            40,
            title,
            font=r.font_l,
            align_y_center=False,
        )

        # Statistics
        total = summary_data.get("total", 0)
        max_day = summary_data.get("max", 0)
        avg_day = summary_data.get("avg", 0)

        stats_y = 120

        # Total contributions
        r.draw_centered_text(
            draw,
            width // 2,
            stats_y,
            str(total),
            font=r.font_xl,
            align_y_center=True,
        )
        r.draw_centered_text(
            draw,
            width // 2,
            stats_y + 60,
            "Total Contributions",
            font=r.font_m,
            align_y_center=True,
        )

        # Detailed statistics (Max / Avg)
        detail_y = stats_y + 140
        detail_text = f"Max Day: {max_day}   |   Daily Avg: {avg_day}"
        r.draw_centered_text(
            draw, width // 2, detail_y, detail_text, font=r.font_s, align_y_center=True
        )

        # Bottom greeting message
        r.draw_centered_text(
            draw,
            width // 2,
            height - 40,
            "See you in next year!",
            font=r.font_s,
            align_y_center=True,
        )
