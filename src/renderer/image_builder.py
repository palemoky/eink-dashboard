"""Image builder for generating display images.

This module handles image generation for different display modes.
"""

import logging

from PIL import Image, ImageDraw

from src.config import Config
from src.layouts import DashboardLayout
from src.layouts.poetry import PoetryLayout
from src.layouts.quote import QuoteLayout
from src.providers.wallpaper import WallpaperManager

logger = logging.getLogger(__name__)


class ImageBuilder:
    """Builds images for different display modes.

    Responsibilities:
    - Generate images based on mode and data
    - Handle mode-specific rendering
    - Coordinate with layout classes

    Example:
        >>> builder = ImageBuilder(width=800, height=480)
        >>> image = builder.build("dashboard", data, layout)
    """

    def __init__(self, width: int, height: int):
        """Initialize image builder.

        Args:
            width: Display width in pixels
            height: Display height in pixels
        """
        self.width = width
        self.height = height

    def build(self, mode: str, data: dict, layout: DashboardLayout) -> Image.Image:
        """Build image for a display mode.

        Args:
            mode: Display mode name
            data: Mode-specific data
            layout: DashboardLayout instance

        Returns:
            PIL Image ready for display
        """
        logger.debug(f"Building image for mode: {mode}")

        if mode == "dashboard":
            return self._build_dashboard(data, layout)
        elif mode == "quote":
            return self._build_quote(data)
        elif mode == "poetry":
            return self._build_poetry(data)
        elif mode == "wallpaper":
            return self._build_wallpaper(data)
        elif mode == "holiday":
            return self._build_holiday(data, layout)
        elif mode == "year_end":
            return self._build_year_end(data, layout)
        else:
            logger.warning(f"Unknown mode '{mode}', using dashboard")
            return self._build_dashboard(data, layout)

    def _build_dashboard(self, data: dict, layout: DashboardLayout) -> Image.Image:
        """Build dashboard image."""
        return layout.create_image(self.width, self.height, data)

    def _build_quote(self, data: dict) -> Image.Image:
        """Build quote image."""
        quote_layout = QuoteLayout()
        return quote_layout.create_quote_image(self.width, self.height, data["quote"])

    def _build_poetry(self, data: dict) -> Image.Image:
        """Build poetry image."""
        poetry_layout = PoetryLayout()
        return poetry_layout.create_poetry_image(self.width, self.height, data["poetry"])

    def _build_wallpaper(self, data: dict) -> Image.Image:
        """Build wallpaper image."""
        wallpaper_manager = WallpaperManager()
        wallpaper_name = Config.display.wallpaper_name or None
        return wallpaper_manager.create_wallpaper(self.width, self.height, wallpaper_name)

    def _build_holiday(self, data: dict, layout: DashboardLayout) -> Image.Image:
        """Build holiday greeting image."""
        holiday = data["holiday"]
        image_mode = "L" if Config.hardware.use_grayscale else "1"
        image = Image.new(image_mode, (self.width, self.height), 255)
        draw = ImageDraw.Draw(image)

        layout.renderer.draw_full_screen_message(
            draw,
            self.width,
            self.height,
            holiday["title"],
            holiday["message"],
            holiday.get("icon"),
        )
        return image

    def _build_year_end(self, data: dict, layout: DashboardLayout) -> Image.Image:
        """Build year-end summary image."""
        image_mode = "L" if Config.hardware.use_grayscale else "1"
        image = Image.new(image_mode, (self.width, self.height), 255)
        draw = ImageDraw.Draw(image)

        layout._draw_year_end_summary(draw, self.width, self.height, data["github_year_summary"])
        return image
