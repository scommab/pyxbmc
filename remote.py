
from pyxbmc import xbmc

import argparse
import sys
import pprint

commands = {
  "play": "play",
  "pause": "pause",
  "stop": "stop",
  "left": "nav_left",
  "right": "nav_right",
  "up": "nav_up",
  "down": "nav_down",
  "back": "nav_back",
  "select": "nav_select",
  "menu": "nav_menu",
  "osd": "nav_show_osd",
  "ping": "ping"
}

parser = argparse.ArgumentParser(description="remote.py")
parser.add_argument("host",
                    help="The XBMC host and port")
parser.add_argument("command",
                    help="The command to send")
args = parser.parse_args()
if not args.command in commands:
  print("Invalid Command")
  print("Command List:")
  for k in sorted(commands.keys()):
    print("\t- %s" % k)
  sys.exit()

connection = xbmc.XBMC(args.host)
r = getattr(connection, commands[args.command])()
worked = False
if r == True:
  worked = True
elif r == False or r is None:
  worked = False
elif "result" in r and r["result"] == "OK":
  worked = True
elif "result" in r and r["result"] == "pong":
  worked = True

if worked:
  print("Worked")
else:
  print("Failed")
