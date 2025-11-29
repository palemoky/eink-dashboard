"""Unit tests for Phase 3 architecture improvements."""

import pytest

from src.core.display_mode import DisplayMode, DisplayModeRegistry
from src.core.events import Event, EventBus, EventType


class TestDisplayModeRegistry:
    """Tests for display mode plugin system."""

    @pytest.fixture
    def registry(self):
        """Create fresh registry for each test."""
        return DisplayModeRegistry()

    def test_register_mode(self, registry):
        """Test mode registration."""

        class TestMode(DisplayMode):
            @property
            def name(self) -> str:
                return "test_mode"

            async def fetch_data(self, **kwargs):
                return {}

            def render(self, width, height, data):
                from PIL import Image

                return Image.new("1", (width, height), 255)

        registry.register(TestMode)
        mode = registry.get("test_mode")
        assert mode is not None
        assert mode.name == "test_mode"

    def test_find_active_mode(self, registry):
        """Test finding active mode."""

        class AlwaysActiveMode(DisplayMode):
            @property
            def name(self) -> str:
                return "always_active"

            def should_activate(self, **kwargs) -> bool:
                return True

            async def fetch_data(self, **kwargs):
                return {}

            def render(self, width, height, data):
                from PIL import Image

                return Image.new("1", (width, height), 255)

        registry.register(AlwaysActiveMode)
        active = registry.find_active_mode()
        assert active is not None
        assert active.name == "always_active"


class TestEventBus:
    """Tests for event system."""

    @pytest.fixture
    def event_bus(self):
        """Create fresh event bus for each test."""
        bus = EventBus()
        yield bus
        bus.clear()

    @pytest.mark.asyncio
    async def test_publish_subscribe(self, event_bus):
        """Test basic pub/sub."""
        received_events = []

        async def handler(event: Event):
            received_events.append(event)

        event_bus.subscribe(EventType.CONFIG_CHANGED, handler)
        await event_bus.emit(EventType.CONFIG_CHANGED, {"key": "value"})

        assert len(received_events) == 1
        assert received_events[0].type == EventType.CONFIG_CHANGED
        assert received_events[0].data == {"key": "value"}

    @pytest.mark.asyncio
    async def test_multiple_handlers(self, event_bus):
        """Test multiple handlers for same event."""
        call_count = 0

        async def handler1(event: Event):
            nonlocal call_count
            call_count += 1

        async def handler2(event: Event):
            nonlocal call_count
            call_count += 1

        event_bus.subscribe(EventType.MODE_CHANGED, handler1)
        event_bus.subscribe(EventType.MODE_CHANGED, handler2)
        await event_bus.emit(EventType.MODE_CHANGED)

        assert call_count == 2

    @pytest.mark.asyncio
    async def test_unsubscribe(self, event_bus):
        """Test unsubscribing from events."""
        call_count = 0

        async def handler(event: Event):
            nonlocal call_count
            call_count += 1

        event_bus.subscribe(EventType.TASK_STARTED, handler)
        await event_bus.emit(EventType.TASK_STARTED)
        assert call_count == 1

        event_bus.unsubscribe(EventType.TASK_STARTED, handler)
        await event_bus.emit(EventType.TASK_STARTED)
        assert call_count == 1  # Not incremented
