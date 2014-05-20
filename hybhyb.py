#!/usr/bin/python

from embed import embed_data
import arg_handler
import constants

#
# Main execution of program happens here
#


# TODO: Parse input from command line


# Just looking for help?
# if flag == -h, then show help


# TODO: Set up our data to pass on to the embed_data function
data = { "cover_obj": "cover_objects/PinkieCrazy.PNG", "target_obj": "blah", "key": "testKey",
         "method": constants.LSB, "stats_mode": False, "show_image": False,
         "message": "You shall not pass!", "garbage": False }

embed_data(data)
