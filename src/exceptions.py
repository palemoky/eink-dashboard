"""Custom exception classes for the E-Ink dashboard application.

This module defines a hierarchy of exceptions for better error handling
and more informative error messages throughout the application.
"""


class DashboardError(Exception):
    """Base exception for all dashboard-related errors."""

    pass


class ProviderError(DashboardError):
    """Exception raised when a data provider fails to fetch data.

    This includes API failures, network errors, or invalid responses.
    """

    def __init__(self, provider: str, message: str, original_error: Exception | None = None):
        self.provider = provider
        self.original_error = original_error
        super().__init__(f"{provider} provider error: {message}")


class CacheError(DashboardError):
    """Exception raised when cache operations fail.

    This includes read/write failures or cache corruption.
    """

    pass


class StateError(DashboardError):
    """Exception raised when state management operations fail.

    This includes state persistence or retrieval failures.
    """

    pass


class ConfigError(DashboardError):
    """Exception raised when configuration is invalid or missing.

    This includes validation errors or missing required configuration.
    """

    pass


class DisplayError(DashboardError):
    """Exception raised when display operations fail.

    This includes driver errors or rendering failures.
    """

    pass


class LayoutError(DashboardError):
    """Exception raised when layout rendering fails.

    This includes component rendering errors or invalid layout data.
    """

    pass
