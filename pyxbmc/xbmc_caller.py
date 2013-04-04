
import requests
import urllib

import json
import sys
import urlparse
import pprint

url = None

def set_url(hostname, port):
  global url
  url = "http://%s:%s/jsonrpc" % (hostname, port)


def call_XBMC(payload):
  if url is None:
    print "!!! set the url var first"
    return {}
  headers = { "Content-Type":"application/json" }
  p = requests.post(url, data=json.dumps(payload), headers=headers)
  return json.loads(p.content)

def xbmc_call(fn):
  def wrapped(*arg, **kwargs):
    return call_XBMC(fn(*arg, **kwargs))
  return wrapped


