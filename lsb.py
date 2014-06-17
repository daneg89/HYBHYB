#!/usr/bin/python

import random

def lsb_decode(target_data, header_len, key=""):
   """ Performs a Least Significant Bit decoding of a stego object

   Params:
      target_data - List of bytes of the target object
      header_len - # of bits used to indicate hidden message length
      key - Password that determines the seed for the random num generator

   Returns:
      List of bits representing the plaintext bit and the embedded message

   """

   target_len = len(target_data)

   # Establish the decoding sequence
   if key == "": # Sequentially
      decode_sequence = range(0, target_len)
   else: # Randomly
      random.seed(key)
      decode_sequence = random.sample(range(0, target_len), target_len - 1)

   # Read header, get length of the message
   header_bits = ""
   for i in range(0, header_len):
      header_bits += str(target_data[decode_sequence[i]] & 1)

   embed_len = int(header_bits, base=2)
   # +1 is to account for the plaintext bit
   decode_sequence = decode_sequence[header_len:embed_len + header_len + 1]

   # Read the bits from the image
   decoded_data = [str(target_data[loc] & 1) for loc in decode_sequence]

   return ''.join(decoded_data)

def lsb_embed(cover_data, target_data, key=""):
   """ Performs a Least Significant Bit embedding of a cover object

   Params:
      cover_data - List of bytes of the cover object
      target_data - String of bits that will be embedded into the cover object
      key - Password that determines the seed for the random num generator

   Returns:
      List of bytes represented as integers encoded using LSB 
   """ 
   embed_len = len(target_data)
   cover_len = len(cover_data)

   # Embed the header
   if key == "": # Sequentially
      embed_sequence = range(0, cover_len)
   else: # Randomly
      random.seed(key)
      embed_sequence = random.sample(range(0, cover_len), cover_len - 1)

   # Slice off the values we don't need
   embed_sequence = embed_sequence[0:embed_len]

   # Embed the target_data
   for i in range(0, embed_len):
      target_lsb = cover_data[embed_sequence[i]] & 1
      if target_lsb > int(target_data[i], 2):
         cover_data[embed_sequence[i]] -= 1;
      elif target_lsb < int(target_data[i], 2):
         cover_data[embed_sequence[i]] += 1;
      else:
         pass

   return cover_data
