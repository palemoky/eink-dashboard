import logging
from pathlib import Path

from PIL import Image

logger = logging.getLogger(__name__)


class MockEPDDriver:
    def __init__(self, width: int = 800, height: int = 480):
        self.width = width
        self.height = height
        logger.info(f"Mock EPD initialized with size {width}x{height}")

    def init(self, fast: bool = False) -> None:
        refresh_mode = "fast" if fast else "full"
        logger.info(f"Mock EPD: init ({refresh_mode} refresh)")

    def clear(self) -> None:
        logger.info("Mock EPD: clear")

    def sleep(self) -> None:
        logger.info("Mock EPD: sleep")

    def display(self, image: Image.Image) -> None:
        logger.info(f"[Mock] Displaying image ({image.width}x{image.height})")
        # Save to file for debugging
        output_path = Path("mock_display_output.png")
        image.save(output_path)
        logger.info(f"[Mock] Saved display output to {output_path}")

    def display_partial(self, image: Image.Image, x: int, y: int, w: int, h: int) -> None:
        logger.info(f"[Mock] Partial display at ({x},{y}) size ({w}x{h})")
        # For mock, just save the partial image
        output_path = Path(f"mock_partial_{x}_{y}_{w}x{h}.png")
        image.save(output_path)
        logger.info(f"[Mock] Saved partial output to {output_path}")
