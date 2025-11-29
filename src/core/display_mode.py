"""Display mode plugin system for extensible display modes.

This module provides an abstract base class for display modes and a registry
system for plugin-based architecture.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Type

from PIL import Image

logger = logging.getLogger(__name__)


class DisplayMode(ABC):
    """Abstract base class for display modes.

    Each display mode implements data fetching and rendering logic.
    New display modes can be added by subclassing this class.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name for this display mode."""
        pass

    @property
    def refresh_interval(self) -> int:
        """Refresh interval in seconds (0 = no auto-refresh)."""
        return 0

    @abstractmethod
    async def fetch_data(self, **kwargs) -> dict[str, Any]:
        """Fetch data required for this display mode.

        Args:
            **kwargs: Additional context (e.g., client, config)

        Returns:
            Dictionary containing all data needed for rendering
        """
        pass

    @abstractmethod
    def render(self, width: int, height: int, data: dict[str, Any]) -> Image.Image:
        """Render the display mode to an image.

        Args:
            width: Display width in pixels
            height: Display height in pixels
            data: Data dictionary from fetch_data()

        Returns:
            PIL Image ready for display
        """
        pass

    def should_activate(self, **kwargs) -> bool:
        """Check if this mode should be activated.

        Override this to implement activation conditions (e.g., time-based, date-based).

        Args:
            **kwargs: Context for decision (e.g., current_time, config)

        Returns:
            True if this mode should be active
        """
        return False


class DisplayModeRegistry:
    """Registry for display mode plugins.

    Manages registration and retrieval of display modes.
    """

    def __init__(self):
        self._modes: dict[str, Type[DisplayMode]] = {}
        self._instances: dict[str, DisplayMode] = {}

    def register(self, mode_class: Type[DisplayMode]) -> None:
        """Register a display mode class.

        Args:
            mode_class: DisplayMode subclass to register
        """
        # Create instance to get name
        instance = mode_class()
        name = instance.name

        if name in self._modes:
            logger.warning(f"Display mode '{name}' already registered, overwriting")

        self._modes[name] = mode_class
        self._instances[name] = instance
        logger.info(f"Registered display mode: {name}")

    def get(self, name: str) -> DisplayMode | None:
        """Get display mode instance by name.

        Args:
            name: Display mode name

        Returns:
            DisplayMode instance or None if not found
        """
        return self._instances.get(name)

    def get_all(self) -> dict[str, DisplayMode]:
        """Get all registered display modes.

        Returns:
            Dictionary of name -> DisplayMode instance
        """
        return self._instances.copy()

    def find_active_mode(self, **kwargs) -> DisplayMode | None:
        """Find the first mode that should be activated.

        Modes are checked in registration order.

        Args:
            **kwargs: Context for activation check

        Returns:
            First active DisplayMode or None
        """
        for mode in self._instances.values():
            if mode.should_activate(**kwargs):
                return mode
        return None


# Global registry instance
_registry = DisplayModeRegistry()


def register_mode(mode_class: Type[DisplayMode]) -> Type[DisplayMode]:
    """Decorator to register a display mode.

    Usage:
        @register_mode
        class MyMode(DisplayMode):
            ...
    """
    _registry.register(mode_class)
    return mode_class


def get_registry() -> DisplayModeRegistry:
    """Get the global display mode registry."""
    return _registry
