"""Unified state management for the E-Ink dashboard application.

This module provides a centralized state manager that handles both in-memory
caching and persistent file storage with async I/O operations.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from ..exceptions import StateError

logger = logging.getLogger(__name__)


class StateManager:
    """Manages application state with in-memory cache and file persistence.

    Features:
    - In-memory cache for fast access
    - Async file I/O for persistence
    - Thread-safe operations with locks
    - Automatic state sync on updates

    Example:
        >>> state = StateManager(Path("data"))
        >>> await state.set("hackernews_page", 1)
        >>> page = await state.get("hackernews_page", default=1)
    """

    def __init__(self, state_dir: Path):
        """Initialize state manager.

        Args:
            state_dir: Directory to store state files
        """
        self.state_dir = state_dir
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, Any] = {}
        self._locks: dict[str, asyncio.Lock] = {}
        self._global_lock = asyncio.Lock()

    def _get_lock(self, key: str) -> asyncio.Lock:
        """Get or create a lock for a specific key."""
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]

    def _get_file_path(self, key: str) -> Path:
        """Get file path for a state key."""
        # Sanitize key for filename
        safe_key = key.replace("/", "_").replace("\\", "_")
        return self.state_dir / f"{safe_key}.json"

    async def get(self, key: str, default: Any = None) -> Any:
        """Get state value by key.

        First checks in-memory cache, then falls back to file if not found.

        Args:
            key: State key
            default: Default value if key not found

        Returns:
            State value or default
        """
        # Check cache first
        if key in self._cache:
            logger.debug(f"State cache hit: {key}")
            return self._cache[key]

        # Load from file
        async with self._get_lock(key):
            file_path = self._get_file_path(key)
            if not file_path.exists():
                logger.debug(f"State not found: {key}, using default")
                return default

            try:
                # Read file asynchronously
                loop = asyncio.get_event_loop()
                content = await loop.run_in_executor(None, file_path.read_text, "utf-8")
                value = json.loads(content)

                # Update cache
                self._cache[key] = value
                logger.debug(f"State loaded from file: {key}")
                return value

            except Exception as e:
                logger.error(f"Failed to load state {key}: {e}")
                raise StateError(f"Failed to load state {key}") from e

    async def set(self, key: str, value: Any) -> None:
        """Set state value by key.

        Updates both in-memory cache and persists to file.

        Args:
            key: State key
            value: State value (must be JSON-serializable)

        Raises:
            StateError: If persistence fails
        """
        async with self._get_lock(key):
            # Update cache
            self._cache[key] = value

            # Persist to file
            file_path = self._get_file_path(key)
            try:
                # Write file asynchronously
                loop = asyncio.get_event_loop()
                content = json.dumps(value, indent=2, ensure_ascii=False)
                await loop.run_in_executor(None, file_path.write_text, content, "utf-8")
                logger.debug(f"State persisted: {key}")

            except Exception as e:
                logger.error(f"Failed to persist state {key}: {e}")
                raise StateError(f"Failed to persist state {key}") from e

    async def delete(self, key: str) -> None:
        """Delete state value by key.

        Removes from both cache and file storage.

        Args:
            key: State key
        """
        async with self._get_lock(key):
            # Remove from cache
            self._cache.pop(key, None)

            # Remove file
            file_path = self._get_file_path(key)
            if file_path.exists():
                try:
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, file_path.unlink)
                    logger.debug(f"State deleted: {key}")
                except Exception as e:
                    logger.warning(f"Failed to delete state file {key}: {e}")

    async def clear(self) -> None:
        """Clear all state (cache and files)."""
        async with self._global_lock:
            self._cache.clear()

            # Remove all state files
            for file_path in self.state_dir.glob("*.json"):
                try:
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, file_path.unlink)
                except Exception as e:
                    logger.warning(f"Failed to delete state file {file_path}: {e}")

            logger.info("All state cleared")

    def get_sync(self, key: str, default: Any = None) -> Any:
        """Synchronous version of get (cache-only, no file I/O).

        Only checks in-memory cache. Use for performance-critical paths.

        Args:
            key: State key
            default: Default value if key not found

        Returns:
            Cached value or default
        """
        return self._cache.get(key, default)
