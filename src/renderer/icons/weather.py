"""Weather icon rendering.

Provides weather icon drawing functions with file loading and fallback rendering.
"""

import logging
import math

from PIL import Image, ImageDraw

logger = logging.getLogger(__name__)


class WeatherIcons:
    """Handles weather icon rendering."""

    def draw_weather_icon(
        self,
        draw: ImageDraw.ImageDraw,
        x: int,
        y: int,
        icon_name: str,
        size: int = 30,
        icons_dir=None,
    ) -> bool:
        """Draw weather icon (load from file or fallback to code).

        Args:
            draw: PIL ImageDraw object
            x, y: Icon center coordinates
            icon_name: Icon name (sun, rain, snow, thunder, cloud)
            size: Icon size
            icons_dir: Path to icons directory

        Returns:
            bool: Whether successfully loaded from file
        """
        # Try loading from file
        if icons_dir and icons_dir.exists():
            icon_path = icons_dir / f"{icon_name}.png"

            if icon_path.exists():
                try:
                    icon = Image.open(icon_path)

                    # Handle transparency
                    if icon.mode == "P":
                        icon = icon.convert("RGBA")
                    elif icon.mode == "LA":
                        icon = icon.convert("RGBA")

                    if icon.mode == "RGBA":
                        background = Image.new("RGB", icon.size, (255, 255, 255))
                        background.paste(icon, mask=icon.split()[3])
                        icon = background
                    elif icon.mode != "RGB":
                        icon = icon.convert("RGB")

                    icon = icon.convert("1")
                    icon = icon.resize((size, size), Image.Resampling.LANCZOS)

                    paste_x = int(x - size // 2)
                    paste_y = int(y - size // 2)
                    draw._image.paste(icon, (paste_x, paste_y))
                    return True
                except Exception as e:
                    logger.warning(f"Failed to load icon {icon_path}: {e}, using fallback")

        # Fallback to code drawing
        match icon_name:
            case "sun":
                self.draw_sun(draw, x, y, size)
            case "rain":
                self.draw_rain(draw, x, y, size)
            case "snow":
                self.draw_snow(draw, x, y, size)
            case "thunder":
                self.draw_thunder(draw, x, y, size)
            case "cloud" | _:
                self.draw_cloud(draw, x, y, size)
        return False

    def draw_sun(self, draw, x, y, size=20):
        """Draw sun icon."""
        r = size // 3
        draw.ellipse((x - r, y - r, x + r, y + r), outline=0, width=2)
        for i in range(0, 360, 45):
            angle = math.radians(i)
            ray_start = r + (size * 0.125)
            ray_end = r + (size * 0.25)
            x1 = x + math.cos(angle) * ray_start
            y1 = y + math.sin(angle) * ray_start
            x2 = x + math.cos(angle) * ray_end
            y2 = y + math.sin(angle) * ray_end
            draw.line((x1, y1, x2, y2), fill=0, width=2)

    def draw_cloud(self, draw, x, y, size=20):
        """Draw cloud icon."""
        s = size / 40.0
        y = y + (5 * s)

        draw.ellipse(
            (x - 20 * s, y - 5 * s, x, y + 15 * s), fill=255, outline=0, width=max(1, int(2 * s))
        )
        draw.ellipse(
            (x, y - 5 * s, x + 20 * s, y + 15 * s), fill=255, outline=0, width=max(1, int(2 * s))
        )
        draw.ellipse(
            (x - 10 * s, y - 15 * s, x + 10 * s, y + 5 * s),
            fill=255,
            outline=0,
            width=max(1, int(2 * s)),
        )
        draw.rectangle((x - 10 * s, y, x + 10 * s, y + 10 * s), fill=255)

    def draw_rain(self, draw, x, y, size=20):
        """Draw rain icon."""
        self.draw_cloud(draw, x, y, size)
        s = size / 40.0
        y_base = y + (15 * s)
        line_len = 10 * s
        offset = 8 * s

        for dx in [-offset, 0, offset]:
            draw.line(
                (x + dx, y_base + 5 * s, x + dx, y_base + 5 * s + line_len),
                fill=0,
                width=max(1, int(2 * s)),
            )

    def draw_snow(self, draw, x, y, size=20):
        """Draw snow icon."""
        self.draw_cloud(draw, x, y, size)
        s = size / 40.0
        y_base = y + (15 * s)
        r_snow = 2 * s

        positions = [(-12 * s, 5 * s), (-2 * s, 8 * s), (8 * s, 5 * s)]
        for dx, dy in positions:
            draw.ellipse(
                (x + dx, y_base + dy, x + dx + r_snow * 2, y_base + dy + r_snow * 2), fill=0
            )

    def draw_thunder(self, draw, x, y, size=20):
        """Draw thunder icon."""
        self.draw_cloud(draw, x, y, size)
        s = size / 40.0
        y_base = y + (10 * s)

        draw.line((x + 2 * s, y_base, x - 5 * s, y_base + 10 * s), fill=0, width=max(1, int(2 * s)))
        draw.line(
            (x - 5 * s, y_base + 10 * s, x, y_base + 10 * s), fill=0, width=max(1, int(2 * s))
        )
        draw.line(
            (x, y_base + 10 * s, x - 3 * s, y_base + 20 * s), fill=0, width=max(1, int(2 * s))
        )
