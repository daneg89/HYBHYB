#!/usr/bin/python

from arg_handler import parse_args
from embed import embed_data
import arg_handler
import constants
import sys

# TODO: Implement
def show_help():
   """ Shows information related to program execution """
   print "help"

#
# Main execution of program happens here
#


# Just looking for help?
if len(sys.argv) == 1 or sys.argv[1] == "-h":
   show_help() 
else:
   # Parse input from command line
   try:
      data = parse_args(sys.argv)
   except: # TODO: catch exception
      pass

# Test data
   data = { "cover_obj": "cover_objects/test.jpg", "target_obj": "lsb_data", "key": "testKey",
      "method": constants.LSB, "stats_mode": False, "show_image": False,
      "message": "You shall not pass!", "garbage": False }

   embed_data(data)
