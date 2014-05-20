#!/usr/bin/python

def parse_args(args):
   """ Takes a set of command-line args and parses them
 
   Params:
     args - String of command line flags
 
   Returns:
      Dictionary that carries the following information
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

   valid_args(args) 
   # TODO: implement
   pass

def valid_args(args):
   """
 
   Makes sure that the args specified on the command line are valid
 
   Params:
      args - String of command line flags
  
   Returns:
      True/False - args are valid?

   """

   # TODO: implement
   pass
