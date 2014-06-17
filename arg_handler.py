#!/usr/bin/python

from constants import *

def get_action(action_flag):
   """
   Params:
      action_flag - String of a valid action flag

   Returns:
      Integer constant representing the method to use
   """

   if "-e" == action_flag:
      action = ACTION_EMBED
   elif "-x" == action_flag:
      action = ACTION_EXTRACT
   elif "-d" == action_flag:
      action = ACTION_DETECT
   elif "-v" == action_flag:
      action = ACTION_VIS_ATK
   elif "-f" == action_flag:
      action = ACTION_FILTERED_VIS_ATK
   elif "-s" == action_flag:
      action = ACTION_HIST_ATK
   else:
      print "Args validator messed up!"

   return action

def get_method(method_flag):
   """ Gets the method to use

   Params:
      method_flag - String of a valid method flag

   Returns:
      Integer constant representing the method to use
   """

   if "-l" == method_flag:
      method = LSB
   elif "-b" == method_flag:
      method = BPCS
   else:
      print "Args validator messed up!"

   return method

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
         > "show_image": Bool
         > "message": String
         > "garbage": Bool
 
   Throws:
     Exception when args are invalid

   """
   if valid_args(args) == False:
      raise Exception # TODO: make more specific

   action = -1
   actions = ["-e", "-x", "-d", "-v", "-f", "-s"]
   key = ""
   garbage = False
   message = ""
   method = -1
   methods = ["-l", "-b"]
   target_obj = None
   cover_obj = None
   show_image = False

   for flag in args:
      if flag in methods:
         method = get_method(flag)
      elif flag in actions:
         action = get_action(flag)
      elif flag == "-g":
         garbage = True
      elif flag[0:2] == "-k":
         key = flag[2:] 
      elif flag[0:2] == "-m":
         message = flag[2:]
      elif flag == "--show-image":
         show_image = True 
      # Assume at this point that the flag is actually a file
      else:
         if target_obj == None:
            target_obj = flag
         else:
            cover_obj = flag

   if message != "" or garbage == True:
      cover_obj = target_obj
      target_obj = None

   return { "action": action, "cover_obj": cover_obj, "target_obj": target_obj, "key": key, "method": method, "show_image": show_image, "message": message, "garbage": garbage }

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
