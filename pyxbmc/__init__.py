
from xbmc import XBMC


__version__ = "0.0.13"
VERSION = tuple(map(int, __version__.split('.')))
__all__ = [
    "XBMC"
]
