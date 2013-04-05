
from xbmc_caller import set_host
import xbmc


__version__ = "0.0.1"
VERSION = tuple(map(int, __version__.split('.')))
__all__ = [
    "set_host", "xbmc"
]
