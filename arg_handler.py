#!/usr/bin/python

from constants import *

def parse_args(args):
   """ Takes a set of command-line args and parses them
 
   Params:
      args - String of command line flags. Acceptable flags are as follows:
         > -e (embed) OR -x (extract) OR -d (detect) OR -v
            (visual attack) OR -f (filtered visual attack)
         > -l (LSB), or -b (BPCS)
         > -k[key] (LSB only)
         > --show-image
         > -m[message] OR -g (garbage)
         > -s (statistics)
 
   Returns:
      Dictionary that carries the following information
         > "action" : Int
         > "cover_obj": String
         > "target_obj": String
         > "key": String
         > "method": Int
         > "stats_mode": Bool
         > "show_image": Bool
         > "message": String
         > "garbage": Bool
 
   Throws:
     Exception when args are invalid

   """
   print args

   if valid_args(args) == False:
      raise Exception # TODO: make more specific

   # Get the method
   if "-l" in args:
      method = LSB
      for i in range(0, len(args)):
         # Key?
         if "-k" in args[i]:
            key = args[i][2:]
   elif "-b" in args:
      method = BPCS
   else:
      print "Args validator messed up!"

   # Get the action
   if flag == "-e":
      action = ACTION_EMBED
   elif "-x" in args:
      action = ACTION_EXTRACT
   elif "-d" in args:
      action = ACTION_DETECT
   elif "-v" in args:
      action = ACTION_VIS_ATK
   elif "-f" in args:
      actoin = ACTION_FILTERED_VIS_ATK

   print "LSB"
   print key


def valid_args(args):
   """
 
   Makes sure that the args specified on the command line are valid
 
   Params:
      args - String of command line flags. Acceptable flags are as follows:
         > -e (embed) OR -x (extract) OR -d (detect) [--histogram] OR -v
            (visual attack) OR -f (filtered visual attack)
         > -l (LSB), or -b (BPCS)
         > -k[key] (LSB only)
         > --show-image
         > -m[message] OR -g (garbage)
         > -s (statistics)
  
   Returns:
      True/False - args are valid?

   """

   # TODO: implement
   pass
