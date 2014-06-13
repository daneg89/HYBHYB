#!/usr/bin/python

def init():
   """ Initialize some things to make things run smoothly """
   sys.path.append("steganalysis")
   sys.path.append("utils")

# TODO: Implement
def show_help():
   """ Shows information related to program execution """
   print "help"

#
# Main execution of program happens here
#

import sys
init()

from arg_handler import parse_args
from decode import decode_data
from embed import embed_data
from visual import filtered_visual_attack
from visual import visual_attack
import arg_handler
import constants

# Just looking for help?
if len(sys.argv) == 1 or sys.argv[1] == "-h":
   show_help() 
else:
   # Parse input from command line
   data = parse_args(sys.argv[1:]) # First arg isn't needed

   if data["action"] == constants.ACTION_EMBED:
      embed_data(data)
   elif data["action"] == constants.ACTION_EXTRACT:
      decode_data(data)
   elif data["action"] == constants.ACTION_FILTERED_VIS_ATK:
      filtered_visual_attack(data["target_obj"])
   elif data["action"] == constants.ACTION_VIS_ATK:
      visual_attack(data["target_obj"])
   else:
      print "Invalid action specified!"
