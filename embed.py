#!/usr/bin/python

from lsb import lsb_embed
from bpcs import bpcs_embed
import constants

#
# Estimates the embedding capacity of the specified object
#
# Params:
#  num_bytes - The number of bits to embed
#  method - The method used to embed the bytes
#
def est_embed_capacity(num_bits, method):
   if method == constants.LSB or method == constants.LSB_PR:
      return num_bits / 8 # ~12.5%
   elif method == constants.BPCS:
      return num_bits / 4 # 25%
   else:
      return 0

#
# Generic embedding function that determines how to embed a file
#
# Params:
#   data - Dictionary that carries the following information
#          > "cover_obj": String
#          > "target_obj": String
#          > "key": String
#          > "method": Int
#          > "stats_mode": Bool
#          > "show_image": Bool
#          > "message": String
#          > "garbage": Bool
#
def embed_data(data):
   lsb_embed(None, None)
   bpcs_embed(None, None)

#
# Generates a random message for the purpose of testing the effectiveness
# of the program. Message will be about 98-99% of the embedding capacity
# that we specify.
#
# Params:
#  embed_capacity - Number of bits that the target object can have modified
#
def generate_message(embed_capacity):
   pass
