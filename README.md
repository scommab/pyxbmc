pyxbmc
======

Python Library for working with the xbmc web api

To Install:

    pip install -e git://github.com/scommab/pyxbmc.git#egg=pyxbmc

Simple Usage:

    from pyxbmc import XBMC

    connection = XBMC("media-server:8080")
    print connection.nav_left()
  

For example usage see:
* ``remote.py``: A simple XBMC command line remote
* ``query.py``: An XBMC command line query tool
