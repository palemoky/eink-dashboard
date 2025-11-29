"""Event system for inter-component communication.

This module provides an event bus for decoupled communication between
components using the observer pattern.
"""

import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Enumeration of event types."""

    # Configuration events
    CONFIG_CHANGED = "config_changed"
    CONFIG_RELOADED = "config_reloaded"

    # Display mode events
    MODE_CHANGED = "mode_changed"
    MODE_ACTIVATED = "mode_activated"
    MODE_DEACTIVATED = "mode_deactivated"

    # Time-based events
    QUIET_HOURS_ENTERED = "quiet_hours_entered"
    QUIET_HOURS_EXITED = "quiet_hours_exited"

    # Task events
    TASK_STARTED = "task_started"
    TASK_STOPPED = "task_stopped"
    TASK_FAILED = "task_failed"

    # Display events
    DISPLAY_REFRESHED = "display_refreshed"
    PARTIAL_REFRESH = "partial_refresh"
    FULL_REFRESH = "full_refresh"


@dataclass
class Event:
    """Event data container.

    Attributes:
        type: Event type
        data: Event-specific data
        source: Component that emitted the event
    """

    type: EventType
    data: dict[str, Any]
    source: str | None = None


# Type alias for event handlers
EventHandler = Callable[[Event], Coroutine[Any, Any, None]]


class EventBus:
    """Event bus for publish-subscribe pattern.

    Allows components to communicate without tight coupling.
    """

    def __init__(self):
        self._handlers: dict[EventType, list[EventHandler]] = defaultdict(list)
        self._lock = asyncio.Lock()

    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Subscribe to an event type.

        Args:
            event_type: Type of event to listen for
            handler: Async function to call when event occurs
        """
        self._handlers[event_type].append(handler)
        logger.debug(f"Subscribed to {event_type.value}: {handler.__name__}")

    def unsubscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Unsubscribe from an event type.

        Args:
            event_type: Type of event
            handler: Handler to remove
        """
        if handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)
            logger.debug(f"Unsubscribed from {event_type.value}: {handler.__name__}")

    async def publish(self, event: Event) -> None:
        """Publish an event to all subscribers.

        Args:
            event: Event to publish
        """
        handlers = self._handlers.get(event.type, [])

        if not handlers:
            logger.debug(f"No handlers for event: {event.type.value}")
            return

        logger.debug(f"Publishing event: {event.type.value} (source: {event.source})")

        # Call all handlers concurrently
        tasks = [handler(event) for handler in handlers]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Log any exceptions
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                handler_name = handlers[i].__name__
                logger.error(f"Error in event handler {handler_name}: {result}")

    async def emit(
        self, event_type: EventType, data: dict[str, Any] | None = None, source: str | None = None
    ) -> None:
        """Convenience method to create and publish an event.

        Args:
            event_type: Type of event
            data: Event data (optional)
            source: Event source (optional)
        """
        event = Event(type=event_type, data=data or {}, source=source)
        await self.publish(event)

    def clear(self) -> None:
        """Clear all event handlers."""
        self._handlers.clear()
        logger.info("Cleared all event handlers")


# Global event bus instance
_event_bus = EventBus()


def get_event_bus() -> EventBus:
    """Get the global event bus instance."""
    return _event_bus


def on_event(event_type: EventType):
    """Decorator to register an event handler.

    Usage:
        @on_event(EventType.CONFIG_CHANGED)
        async def handle_config_change(event: Event):
            print(f"Config changed: {event.data}")
    """

    def decorator(func: EventHandler) -> EventHandler:
        _event_bus.subscribe(event_type, func)
        return func

    return decorator
