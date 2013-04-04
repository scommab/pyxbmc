from xbmc_caller import xbmc_call
import json
import sys
import urlparse
import pprint


def make_call(method, params=None):
  r = {"jsonrpc": "2.0", "method": method, "id": 1}
  if not params is None:
    r["params"] = params
  return r

@xbmc_call
def get_active_players():
  return make_call("Player.GetActivePlayers")

@xbmc_call
def get_addons():
  return make_call("Addons.GetAddons")

@xbmc_call
def get_playlists():
  return make_call("Playlist.GetPlaylists")

@xbmc_call
def get_movies():
  return make_call("VideoLibrary.GetMovies")

@xbmc_call
def get_tv_shows():
  return make_call("VideoLibrary.GetTVShows")

@xbmc_call
def get_tv_seasons(tvshowid):
  return make_call("VideoLibrary.GetSeasons", {
    "tvshowid": tvshowid
  })

@xbmc_call
def get_tv_episodes(tvshowid=None, season=None):
  params = {}
  if not tvshowid is None:
    params["tvshowid"] = tvshowid
  if not season is None:
    params["season"] = season
  return make_call("VideoLibrary.GetEpisodes", params)

@xbmc_call
def get_music_artists():
  return make_call("AudioLibrary.GetArtists")

@xbmc_call
def get_music_album(artistid):
  return make_call("AudioLibrary.GetAlbums", {
    "filter": {"artistid": artistid}
  })

@xbmc_call
def clear_playlist(playlist):
  return make_call("Playlist.Clear", {
    "playlistid": playlist
  })

@xbmc_call
def add_to_playlist(playlist, link):
  return make_call("Playlist.Add", {
    "playlistid": playlist,
    "item": {"file": link}
  })

@xbmc_call
def play_item(playlist, pos=1):
  return make_call("Player.Open", {
  "item": {
      "playlistid": playlist,
      "position": pos
  }})

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

def get_show_season_episodes(showid):
  d = get_tv_seasons(showid)
  result = []
  seasons = d["result"]["seasons"]
  for i in range(len(seasons)):
    season = seasons[i]
    episodes = get_tv_episodes(showid, i+1) # 1 based wtf?
    episodes = episodes["result"]["episodes"]
    season["episodes"] = episodes
    result.append(season)
  return result

