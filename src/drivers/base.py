from typing import Protocol, runtime_checkable

from PIL import Image


@runtime_checkable
class EPDDriver(Protocol):
    width: int
    height: int

    def init(self) -> None:
        """Initialize the display"""
        ...

    def clear(self) -> None:
        """Clear the display"""
        ...

    def sleep(self) -> None:
        """Put the display to sleep"""
        ...

    def display(self, image: Image.Image) -> None:
        """Display a PIL Image"""
        ...

    def display_partial(self, image: Image.Image, x: int, y: int, w: int, h: int) -> None:
        """Display a PIL Image in a partial region.

        Args:
            image: PIL Image to display
            x: X coordinate of top-left corner
            y: Y coordinate of top-left corner
            w: Width of the region
            h: Height of the region
        """
        ...
