from xbmc_caller import xbmc_call
import urlparse


def make_call(method, params=None):
  r = {"jsonrpc": "2.0", "method": method, "id": 1}
  if not params is None:
    r["params"] = params
  return r

@xbmc_call
def ping():
  return make_call("JSONRPC.Ping")

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

@xbmc_call
def player_play_pause(player):
  return make_call("Player.PlayPause",
      {"playerid": player})

@xbmc_call
def player_stop(player):
  return make_call("Player.Stop",
      {"playerid": player})

@xbmc_call
def get_player_properties(player, properties=None):
  if properties is None:
    properties = [
      "speed", "playlistid",
      "time", "totaltime",
      "percentage"
    ]
  return make_call("Player.GetProperties", {
    "playerid": player,
    "properties": properties
  })

@xbmc_call
def nav_down():
  return make_call("Input.Down")

@xbmc_call
def nav_up():
  return make_call("Input.Up")

@xbmc_call
def nav_left():
  return make_call("Input.Left")

@xbmc_call
def nav_right():
  return make_call("Input.Right")

@xbmc_call
def nav_back():
  return make_call("Input.Back")

@xbmc_call
def nav_menu():
  return make_call("Input.ContextMenu")

@xbmc_call
def nav_select():
  return make_call("Input.Select")

@xbmc_call
def nav_menu():
  return make_call("Input.Menu")

@xbmc_call
def nav_show_osd():
  return make_call("Input.ShowOSD")

@xbmc_call
def nav_send_text(text, complete=False):
  return make_call("Input.SendText", {"text": text, "done": complete})

@xbmc_call
def nav_execute(action):
  return make_call("Input.ExecuteAction", {"action": action})

def make_youtube_link(video_id):
  return "plugin://plugin.video.youtube/" + \
         "?action=play_video&videoid=%s" % video_id

def play_youtube(video_id):
  if "http" in video_id:
    # decode youtube url
    q = urlparse.parse_qs(urlparse.urlparse(video_id).query)
    video_id = q["v"][0]
  d = get_playlists()
  playlist_id = None
  for playlist in d["result"]:
    if playlist["type"] == "video":
      playlist_id = playlist["playlistid"]

  clear_playlist(playlist_id)
  add_to_playlist(playlist_id, make_youtube_link(video_id))
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
    episodes = get_tv_episodes(showid, i+1)  # 1 based wtf?
    episodes = episodes["result"]["episodes"]
    season["episodes"] = episodes
    result.append(season)
  return result


def is_playing(player_id=None):
  if player_id is None:
    d = get_active_players()
    if not "result" in d or len(d["result"]) == 0:
      return False
    player_id = d["result"][0]["playerid"]
  props = get_player_properties(player_id, ["speed"])
  return props["result"]["speed"] != 0

def play(player_id=None):
  if player_id is None:
    d = get_active_players()
    if not "result" in d or len(d["result"]) == 0:
      return None
    player_id = d["result"][0]["playerid"]
  if is_playing(player_id):
    return True
  d = player_play_pause(player_id)
  return d["result"]["speed"] != 0

def pause(player_id=None):
  if player_id is None:
    d = get_active_players()
    if not "result" in d or len(d["result"]) == 0:
      return None
    player_id = d["result"][0]["playerid"]
  if not is_playing(player_id):
    return True
  d = player_play_pause(player_id)
  return d["result"]["speed"] == 0

def stop():
  d = get_active_players()
  if d["result"] and len(d["result"]) > 0:
    player_id = d["result"][0]["playerid"]
    d = player_stop(player_id)
    return d["result"] == "OK"
  return None


