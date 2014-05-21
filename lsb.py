#!/usr/bin/python

import random

# TODO: Add header_bit_len
def lsb_embed(target_data, data, is_random=False, key=""):
   """ Performs a Least Significant Bit embedding of a cover object

   Params:
      target_data - Collection of byte strings of the cover object
      data - String of bits that will be embedded into the cover object
      is_random - Determines if embedding is sequential or pseudo-random
      key - Password that determines the seed for the random num generator

   Returns:

   """ 

   bit_header = 2 # TODO: Move to param list, no default
   embed_len = len(data) + bit_header

   if is_random:
      random.seed(key) 
      embed_sequence = random.sample(range(0, len(target_data)), 
                                           embed_len)
   else:
      embed_sequence = range(0, embed_len)

   print "Data before embedding"
   print target_data
   print data

   print embed_len
   print embed_sequence

   # TODO: Change len(data) to embed_len
   for i in range(0, len(data)):
      # TODO: replace last bit of target data with bit
      target_data[embed_sequence[i]] = data[i]



   print ("Data after embedding")
   print target_data
   print data
