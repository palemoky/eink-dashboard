"""Time slot parsing and management utilities.

This module provides elegant time slot parsing and checking functionality.
"""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TimeSlot:
    """Represents a time slot with start and end hours.

    Attributes:
        start: Start hour (0-23)
        end: End hour (0-23, can be 0 for cross-day slots)
    """

    start: int
    end: int

    def __post_init__(self):
        """Validate time slot values."""
        if not (0 <= self.start <= 23):
            raise ValueError(f"Start hour must be 0-23, got {self.start}")
        if not (0 <= self.end <= 23):
            raise ValueError(f"End hour must be 0-23, got {self.end}")

    def contains(self, hour: int) -> bool:
        """Check if an hour is within this time slot.

        Args:
            hour: Hour to check (0-23)

        Returns:
            True if hour is within the slot
        """
        if self.start > self.end:  # Cross-day slot (e.g., 20-8)
            return hour >= self.start or hour < self.end
        elif self.start == self.end == 0:  # Special case: midnight
            return hour == 0
        else:  # Same-day slot
            return self.start <= hour < self.end

    def __str__(self) -> str:
        return f"{self.start:02d}-{self.end:02d}"


class TimeSlots:
    """Manages multiple time slots for time-based activation.

    Example:
        >>> slots = TimeSlots("0-12,18-24")
        >>> slots.contains_hour(10)  # True
        >>> slots.contains_hour(15)  # False
    """

    def __init__(self, slots_str: str):
        """Initialize time slots from string.

        Args:
            slots_str: Time slots string (e.g., "0-12,18-24" or "20-8")
        """
        self.slots_str = slots_str
        self.slots = self._parse(slots_str)

    def _parse(self, slots_str: str) -> list[TimeSlot]:
        """Parse time slots string into TimeSlot objects.

        Args:
            slots_str: Time slots string

        Returns:
            List of TimeSlot objects
        """
        if not slots_str:
            return []

        slots = []
        try:
            for slot in slots_str.split(","):
                slot = slot.strip()
                if "-" not in slot:
                    continue

                start_str, end_str = slot.split("-")
                start = int(start_str)
                end = int(end_str)

                # Handle end=24 as midnight (0)
                if end == 24:
                    end = 0

                slots.append(TimeSlot(start, end))

        except (ValueError, AttributeError) as e:
            logger.warning(f"Failed to parse time slots '{slots_str}': {e}")
            return []

        return slots

    def contains_hour(self, hour: int) -> bool:
        """Check if an hour is within any of the time slots.

        Args:
            hour: Hour to check (0-23)

        Returns:
            True if hour is within any slot
        """
        if not (0 <= hour <= 23):
            raise ValueError(f"Hour must be 0-23, got {hour}")

        return any(slot.contains(hour) for slot in self.slots)

    def __bool__(self) -> bool:
        """Check if any slots are defined."""
        return bool(self.slots)

    def __str__(self) -> str:
        return self.slots_str

    def __repr__(self) -> str:
        return f"TimeSlots({self.slots_str!r})"
