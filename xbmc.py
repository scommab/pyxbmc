
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

@xbmc_call
def get_players():
  return {"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id" : 1}
@xbmc_call
def get_playlists():
  return {"jsonrpc": "2.0", "method": "Playlist.GetPlaylists", "id" : 1}
@xbmc_call
def get_movies():
  return {"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "id" : 1}
@xbmc_call
def get_tv_shows():
  return {"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "id" : 1}
@xbmc_call
def get_tv_seasons(tvshowid):
  return {"jsonrpc": "2.0", 
      "method": "VideoLibrary.GetSeasons",
      "params": {
        "tvshowid": tvshowid
        },
      "id" : 1}
@xbmc_call
def get_tv_episodes(tvshowid=None, season=None):
  params = {}
  if not tvshowid is None:
    params["tvshowid"] = tvshowid
  if not season is None:
    params["season"] = season
  return {"jsonrpc": "2.0", 
      "method": "VideoLibrary.GetEpisodes",
      "params": params,
      "id" : 1}
@xbmc_call
def get_music_artists():
  return {"jsonrpc": "2.0", "method": "AudioLibrary.GetArtists", "id" : 1}

@xbmc_call
def get_music_album(artistid):
  return {"jsonrpc": "2.0",
      "method": "AudioLibrary.GetAlbums",
      "params": {"filter": {"artistid": artistid}},
      "id" : 1}


@xbmc_call
def clear_playlist(playlist):
  return {
      "jsonrpc": "2.0", 
      "method": "Playlist.Clear", 
      "params":{
        "playlistid": playlist, 
        }, 
      "id" : 1
      }

@xbmc_call
def add_to_playlist(playlist, link):
  return {
      "jsonrpc": "2.0", 
      "method": "Playlist.Add", 
      "params":{
        "playlistid": playlist, 
        "item" :{ "file" : link }
        }, 
      "id" : 1
      }

@xbmc_call
def play_item(playlist, pos=1):
  return {
      "jsonrpc": "2.0", 
      "method": "Player.Open", 
      "params":{ "item":{
        "playlistid": playlist, 
        "position" : pos
        }}, 
      "id" : 1
      }

def make_youtube_link(video_id):
  return "plugin://plugin.video.youtube/" + \
         "?action=play_video&videoid=%s" % video_id

def play_youtube(video_id):
  if "http" in videoId:
    # decode youtube url
    q = urlparse.parse_qs(urlparse.urlparse(videoId).query)
    videoId = q["v"][0]
  d = get_playlists()
  playlist_id = None
  for playlist in d["result"]:
    if playlist["type"] == "video":
      playlist_id = playlist["playlistid"]

  clear_playlist(playlist_id)
  add_to_playlist(playlist_id, make_youtube_link(videoId))
  d = play_item(playlist_id)
  return d["result"] == 'OK'

def find_artist(name):
  name = name.lower()
  d = get_music_artists()
  for a in d["result"]["artists"]:
    if a["artist"].lower() == name:
      return a
  return None

def find_tv_show(name):
  name = name.lower()
  d = get_tv_shows()
  for a in d["result"]["tvshows"]:
    if a["label"].lower() == name:
      return a
  return None

if __name__ == "__main__":
  set_url("192.168.1.185","8080")
  a = find_artist("nine inch nails")
  print json.dumps(get_music_album(a["artistid"]), indent=2)
  t = find_tv_show("The Venture Bros.")
  print json.dumps(get_tv_seasons(t["tvshowid"]), indent=2)

