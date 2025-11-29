"""Shape drawing utilities.

Provides functions for drawing progress rings and other shapes.
"""

from PIL import ImageDraw


class ShapeRenderer:
    """Handles shape drawing operations."""

    # Grayscale color constants
    COLOR_BLACK = 0
    COLOR_DARK_GRAY = 128
    COLOR_LIGHT_GRAY = 192
    COLOR_WHITE = 255

    def draw_progress_ring(
        self,
        draw: ImageDraw.ImageDraw,
        x: int,
        y: int,
        radius: int,
        percent: int | float,
        thickness: int = 5,
        use_grayscale: bool = False,
    ):
        """Draw a progress ring with optional grayscale support."""
        ring_color = self.COLOR_DARK_GRAY if use_grayscale else 0
        bg_color = self.COLOR_WHITE

        bbox = (x - radius, y - radius, x + radius, y + radius)
        draw.ellipse(bbox, outline=ring_color, width=1)

        start_angle = -90
        try:
            p = float(percent)
        except ValueError:
            p = 0

        end_angle = -90 + (360 * (p / 100.0))
        if p > 0:
            draw.pieslice(bbox, start=start_angle, end=end_angle, fill=ring_color)

        inner_r = radius - thickness
        draw.ellipse(
            (x - inner_r, y - inner_r, x + inner_r, y + inner_r), fill=bg_color, outline=ring_color
        )
