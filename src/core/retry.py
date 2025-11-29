"""Unified retry strategy for the E-Ink dashboard application.

This module provides a consistent retry decorator for all API calls
with configurable parameters.
"""

import logging
from typing import Callable, TypeVar

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable)


def with_retry(
    max_attempts: int = 3,
    min_wait: float = 1.0,
    max_wait: float = 10.0,
    retry_on: tuple = (httpx.RequestError, httpx.HTTPStatusError),
):
    """Unified retry decorator for API calls.

    Args:
        max_attempts: Maximum number of retry attempts
        min_wait: Minimum wait time between retries (seconds)
        max_wait: Maximum wait time between retries (seconds)
        retry_on: Tuple of exception types to retry on

    Usage:
        @with_retry(max_attempts=5)
        async def api_call():
            ...
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        retry=retry_if_exception_type(retry_on),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )


# Predefined retry strategies for common use cases
api_retry = with_retry(max_attempts=3, min_wait=2.0, max_wait=10.0)
critical_api_retry = with_retry(max_attempts=5, min_wait=1.0, max_wait=30.0)
fast_retry = with_retry(max_attempts=2, min_wait=0.5, max_wait=2.0)
