from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("eink-dashboard")
except PackageNotFoundError:
    __version__ = "unknown"
