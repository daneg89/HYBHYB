#!/usr/bin/python

import random

def lsb_decode(cover_data, header_len, is_random=False, key=""):
   """ Performs a Least Significant Bit decoding of a stego object

   Params:
      cover_data - Collection of byte strings of the cover object
      header_len - # of bits used to indicate hidden message length
      is_random - Determines if decoding is sequential or pseudo-random
      key - Password that determines the seed for the random num generator

   Returns:


   """

   # Set up the decode sequence


   # Read first bit; 1 = PlainText, 0 = Other


   # Read header, get length of the message


   # 

   pass

def lsb_embed(cover_data, data, is_random=False, key=""):
   """ Performs a Least Significant Bit embedding of a cover object

   Params:
      cover_data - List of bytes of the cover object
      data - String of bits that will be embedded into the cover object
      is_random - Determines if embedding is sequential or pseudo-random
      key - Password that determines the seed for the random num generator

   Returns:
      List of bytes represented as integers encoded using LSB 
   """ 
   embed_len = len(data)

   # Set up the embed sequence
   if is_random:
      random.seed(key) 
      embed_sequence = random.sample(range(0, len(cover_data)), 
                                           embed_len)
   else:
      embed_sequence = range(0, embed_len)

   # Embed the data
   for i in range(0, embed_len):
      target_lsb = cover_data[embed_sequence[i]] & 1
      if target_lsb > int(data[i], 2):
         cover_data[embed_sequence[i]] -= 1;
      elif target_lsb < int(data[i], 2):
         cover_data[embed_sequence[i]] += 1;
      else:
         pass

   return cover_data
