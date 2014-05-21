#!/usr/bin/python

import random

def create_header(header_len, message_len):
   """ Creates the header that indicates how long a message is

   Params:
      header_len - Length that the header should be
      message_len - Length of the message that will be embedded

   Returns:
      String header with leading zeroes included

  """

   message_bits = bin(message_len)[2:]
   leading_zeroes = header_len - len(message_bits)

   if leading_zeroes > 0:
      header = (leading_zeroes * "0") + message_bits 
   else:
      header = message_bits

   return header

def lsb_decode(target_data, header_len, is_random=False, key=""):
   """ Performs a Least Significant Bit decoding of a stego object

   Params:
      target_data - Collection of byte strings of the cover object
      header_len - # of bits used to indicate hidden message length
      is_random - Determines if decoding is sequential or pseudo-random
      key - Password that determines the seed for the random num generator

   Returns:


   """
   pass

def lsb_embed(target_data, data, is_random=False, key=""):
   """ Performs a Least Significant Bit embedding of a cover object

   Params:
      target_data - Collection of byte strings of the cover object
      data - String of bits that will be embedded into the cover object
      is_random - Determines if embedding is sequential or pseudo-random
      key - Password that determines the seed for the random num generator

   Returns:

   """ 

   header_len = 2 # TODO: Move to param list, no default
   header_bits = create_header(header_len, len(data))
   embed_message = header_bits + data
   embed_len = len(embed_message)

   if is_random:
      random.seed(key) 
      embed_sequence = random.sample(range(0, len(target_data)), 
                                           embed_len)
   else:
      embed_sequence = range(0, embed_len)

   for i in range(0, len(embed_message)):
      target_lsb = target_data[embed_sequence[i]] & 1
      if target_lsb > int(embed_message[i], 2):
         target_data[embed_sequence[i]] -= 1;
      elif target_lsb < int(embed_message[i], 2):
         target_data[embed_sequence[i]] += 1;
      else:
         pass

   return target_data
