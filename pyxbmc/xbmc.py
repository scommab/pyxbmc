import urllib2
import urlparse
import json


def make_youtube_link(video_id):
  """Takes a video_id and returns an xbmc youtube link"""
  return "plugin://plugin.video.youtube/" + \
         "?action=play_video&videoid=%s" % video_id


class XBMC(object):
  """XBMC Connection Handler."""

  def __init__(self, host):
    """takes XBMC host"""
    self.host = host
    self.url = "http://%s/jsonrpc" % self.host

  def call_XBMC(self, payload):
    """Sends payload to XBMC."""
    req = urllib2.Request(self.url)
    req.add_header("Content-Type", "application/json")
    res = urllib2.urlopen(req, data=json.dumps(payload))
    return json.loads(res.read())

  def make_call(self, method, params=None):
    """Make a standard xbmc call object."""
    r = {"jsonrpc": "2.0", "method": method, "id": 1}
    if not params is None:
      r["params"] = params
    return self.call_XBMC(r)

  def ping(self):
    return self.make_call("JSONRPC.Ping")

  def get_active_players(self):
    return self.make_call("Player.GetActivePlayers")

  def get_addons(self):
    return self.make_call("Addons.GetAddons")

  def get_playlists(self):
    return self.make_call("Playlist.GetPlaylists")

  def get_movies(self):
    return self.make_call("VideoLibrary.GetMovies")

  def get_movie_details(self, movie_id, properties=None):
    if properties is None:
      properties = [
          "plotoutline", "cast", "plot",
          "mpaa", "rating",
          "tagline", "art"
      ]
    return self.make_call("VideoLibrary.GetMovieDetails", {
      "movieid": movie_id,
      "properties": properties
    })

  def get_tv_shows(self):
    return self.make_call("VideoLibrary.GetTVShows")

  def get_tv_show_details(self, tvshow_id, properties=None):
    if properties is None:
      properties = [
          "cast", "genre", "plot",
          "mpaa", "rating",
          "tag", "art"
      ]
    return self.make_call("VideoLibrary.GetTVShowDetails", {
      "tvshowid": tvshow_id,
      "properties": properties
    })

  def get_seasons(self, tvshowid):
    return self.make_call("VideoLibrary.GetSeasons", {
      "tvshowid": tvshowid
    })

  def get_episodes(self, tvshowid=None, season=None):
    params = {}
    if not tvshowid is None:
      params["tvshowid"] = tvshowid
    if not season is None:
      params["season"] = season
    return self.make_call("VideoLibrary.GetEpisodes", params)

  def get_episode_details(self, episode_id, properties=None):
    if properties is None:
      properties = [
          "cast", "showtitle", "plot",
          "season", "tvshowid",
          "firstaired", "art"
      ]
    return self.make_call("VideoLibrary.GetEpisodeDetails", {
      "episodeid": episode_id,
      "properties": properties
    })


  def get_music_artists(self):
    return self.make_call("AudioLibrary.GetArtists")

  def get_music_album(self, artistid):
    return self.make_call("AudioLibrary.GetAlbums", {
      "filter": {"artistid": artistid}
    })

  def clear_playlist(self, playlist):
    return self.make_call("Playlist.Clear", {
      "playlistid": playlist
    })

  def add_to_playlist(self, playlist, link):
    return self.make_call("Playlist.Add", {
      "playlistid": playlist,
      "item": {"file": link}
    })

  def play_item(self, playlist, pos=1):
    return self.make_call("Player.Open", {
    "item": {
        "playlistid": playlist,
        "position": pos
    }})

  def player_play_pause(self, player):
    return self.make_call("Player.PlayPause",
        {"playerid": player})

  def player_stop(self, player):
    return self.make_call("Player.Stop",
        {"playerid": player})

  def get_player_properties(self, player, properties=None):
    if properties is None:
      properties = [
        "speed", "playlistid",
        "time", "totaltime",
        "percentage"
      ]
    return self.make_call("Player.GetProperties", {
      "playerid": player,
      "properties": properties
    })

  def nav_down(self):
    return self.make_call("Input.Down")

  def nav_up(self):
    return self.make_call("Input.Up")

  def nav_left(self):
    return self.make_call("Input.Left")

  def nav_right(self):
    return self.make_call("Input.Right")

  def nav_back(self):
    return self.make_call("Input.Back")

  def nav_menu(self):
    return self.make_call("Input.ContextMenu")

  def nav_select(self):
    return self.make_call("Input.Select")

  def nav_menu(self):
    return self.make_call("Input.Menu")

  def nav_show_osd(self):
    return self.make_call("Input.ShowOSD")

  def nav_send_text(self, text, complete=False):
    return self.make_call("Input.SendText", {"text": text, "done": complete})

  def nav_execute(self, action):
    return self.make_call("Input.ExecuteAction", {"action": action})

  # composite methods

  def play_youtube(self, video_id):
    if "http" in video_id:
      # decode youtube url
      q = urlparse.parse_qs(urlparse.urlparse(video_id).query)
      video_id = q["v"][0]
    d = self.get_playlists()
    playlist_id = None
    for playlist in d["result"]:
      if playlist["type"] == "video":
        playlist_id = playlist["playlistid"]
    self.clear_playlist(playlist_id)
    self.add_to_playlist(playlist_id, make_youtube_link(video_id))
    d = self.play_item(playlist_id)
    return d["result"] == 'OK'

  def find_artist(self, name):
    name = name.lower()
    d = self.get_music_artists()
    for a in d["result"]["artists"]:
      if a["artist"].lower() == name:
        return a
    return None

  def find_tv_show(self, name):
    name = name.lower()
    d = self.get_tv_shows()
    for a in d["result"]["tvshows"]:
      if a["label"].lower() == name:
        return a
    return None

  def find_movie(self, name):
    name = name.lower()
    d = self.get_movies()
    for a in d["result"]["movies"]:
      if a["label"].lower() == name:
        return a
    return None

  def get_show_season_episodes(self, showid):
    d = self.get_seasons(showid)
    result = []
    seasons = d["result"]["seasons"]
    for i in range(len(seasons)):
      season = seasons[i]
      episodes = self.get_episodes(showid, i + 1)  # 1 based wtf?
      episodes = episodes["result"]["episodes"]
      season["episodes"] = episodes
      result.append(season)
    return result

  def is_playing(self, player_id=None):
    if player_id is None:
      d = self.get_active_players()
      if not "result" in d or len(d["result"]) == 0:
        return False
      player_id = d["result"][0]["playerid"]
    props = self.get_player_properties(player_id, ["speed"])
    return props["result"]["speed"] != 0

  def play(self, player_id=None):
    if player_id is None:
      d = self.get_active_players()
      if not "result" in d or len(d["result"]) == 0:
        return None
      player_id = d["result"][0]["playerid"]
    if self.is_playing(player_id):
      return True
    d = self.player_play_pause(player_id)
    return d["result"]["speed"] != 0

  def pause(self, player_id=None):
    if player_id is None:
      d = self.get_active_players()
      if not "result" in d or len(d["result"]) == 0:
        return None
      player_id = d["result"][0]["playerid"]
    if not self.is_playing(player_id):
      return True
    d = self.player_play_pause(player_id)
    return d["result"]["speed"] == 0

  def stop(self, player_id=None):
    if player_id is None:
      d = self.get_active_players()
      if not (d["result"] and len(d["result"]) > 0):
        player_id = d["result"][0]["playerid"]
      else:
        return None
    d = self.player_stop(player_id)
    return d["result"] == "OK"
