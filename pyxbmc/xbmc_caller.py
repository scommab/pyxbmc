import urllib2
import json

url = None


def set_url(hostname, port):
  global url
  url = "http://%s:%s/jsonrpc" % (hostname, port)


def call_XBMC(payload):
  if url is None:
    print "!!! set the url var first"
    return {}
  req = urllib2.Request(url)
  req.add_header("Content-Type", "application/json")
  res = urllib2.urlopen(req, data=json.dumps(payload))
  return json.loads(res.read())


def xbmc_call(fn):
  def wrapped(*arg, **kwargs):
    return call_XBMC(fn(*arg, **kwargs))
  return wrapped
