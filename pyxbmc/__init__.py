
from xbmc import XBMC


__version__ = "0.0.16"
VERSION = tuple(map(int, __version__.split('.')))
__all__ = [
    "XBMC"
]
