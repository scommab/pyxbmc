
from pyxbmc import xbmc

import argparse
import sys
import json

def show(data):
  print json.dumps(data, indent=2, sort_keys=True)


parser = argparse.ArgumentParser(description="query.py")
parser.add_argument("host",
                    help="The XBMC host and port")
parser.add_argument("type",
                    help="The type of object you are looking for",
                    choices=["artists", "albums", "songs",
                             "shows", "episodes", "movies"])
parser.add_argument("-f", "--find", metavar="name",
                    help="Find by name")
parser.add_argument("-d", "--details", metavar="id", type=int,
                    help="Full details on an item")
parser.add_argument("-a", "--all", action="store_true",
                    help="Return all")

args = parser.parse_args()

connection = xbmc.XBMC(args.host)
if args.all:
  if args.type == "artists":
    show(connection.get_artists()["result"]["artists"])
  elif args.type == "albums":
    show(connection.get_albums()["result"]["albums"])
  elif args.type == "songs":
    show(connection.get_songs()["result"]["songs"])
  elif args.type == "shows":
    show(connection.get_tv_shows()["result"]["tvshows"])
  elif args.type == "episodes":
    show(connection.get_episodes()["result"]["episodes"])
  elif args.type == "movies":
    show(connection.get_movies()["result"]["movies"])
elif args.find is not None:
  if args.type == "artists":
    show(connection.find_artist(args.find))
  elif args.type == "albums":
    show(connection.find_album(args.find))
  elif args.type == "songs":
    show(connection.find_song(args.find))
  elif args.type == "shows":
    show(connection.find_tv_show(args.find))
  elif args.type == "episodes":
    show(connection.find_episode(args.find))
  elif args.type == "movies":
    show(connection.find_movie(args.find))
elif args.details is not None:
  show(connection.get_details(args.details, args.type))
else:
  print "No action passed"
