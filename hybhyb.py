#!/usr/bin/python

def init():
   """ Initialize some things to make things run smoothly """
   sys.path.append("steganalysis")
   sys.path.append("utils")

def show_help():
   """ Shows information related to program execution """
   print ("\nUsage: action_flag(s) method_flag(s) optional_flag(s) " +
           "target_obj [cover_obj]")

   print "\nAction Flags:"
   print "   -e: embed a cover object using either a message or a target object"
   print "   -x: extract data from a target object"
   print "   -s: perform a histogram attack on a target object"
   print "   -f: perform a filtered visual attack on a target object"
   print "   -v: perform a visual attack on a target object\n"

   print "Method Flags:"
   print "   -b: Embed using the Bit-Plane Complexity Segmentation (BPCS) method"
   print "   -l: Embed using the Least Significant Bit (LSB) method\n"

   print "Optional Flags:"
   print "   -h: Shows this help dialog"
   print "   -m: replaces target_obj with an ASCII message that the user specifies"
   print "   -g: generates a message of 1s and 0s that fills the entire cover object\n"

   print "Notes:"
   print "   * The ordering of the flags is NOT important"
   print "   * The ordering of target_obj and cover_obj IS important"
   print ("   * When using flags -m and -k, ASCII message/key must immediately" +
          " follow the flag. Example: -kTheKey -mTheMessage")
   print "   * Flags MUST each have their own '-'. i.e. -l -e is valid, -le is not\n"

   print "Examples of Usage:"
   print "   python hybhyb.py -l -e cover_objects/target.png cover_objects/cover.gif"
   print "     - Embeds target.png into cover.gif using LSB"
   print "   python hybhyb.py -l -kStegoKey -mSecret cover_objects/cool.png"
   print ("     - Embeds message 'Secret' into cool.png with key 'StegoKey' " +
          "using Pseudo-random LSB")
   print "   python hybhyb.py -f stego_objects/Steg_cover.gif"
   print "     - Performs a filtered visual attack on Steg_cover.gif\n"

#
# Main execution of program happens here
#

import sys
init()

from arg_handler import parse_args
from decode import decode_data
from embed import embed_data
from histogram import histogram_attack
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
   elif data["action"] == constants.ACTION_HIST_ATK:
      histogram_attack(data["target_obj"])
   else:
      print "Invalid action specified!"
