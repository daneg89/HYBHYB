#!/usr/bin/python

import random

def lsb_decode(target_data, header_len, key=""):
   """ Performs a Least Significant Bit decoding of a stego object

   Params:
      target_data - List of bytes of the target object
      header_len - # of bits used to indicate hidden message length
      key - Password that determines the seed for the random num generator

   Returns:
      List of bits representing the embedded message

   """

   # Decode the header
   if key == "": # Sequentially
      header_sequence = range(0, header_len)
   else: # Randomly
      random.seed(key)
      header_sequence = random.sample(range(0, len(target_data)), header_len)

   header_bits = ""
   for i in range(0, header_len):
      # Read header, get length of the message
      header_bits += str(target_data[header_sequence[i]] & 1)
      embed_len = int(header_bits, base=2)

   # Decode the message
   if key == "": # Sequentially
      main_sequence = range(len(header_sequence), embed_len)
   else: # Randomly
      main_sequence = random.sample(range(0, len(target_data)), embed_len)
      # Remove duplicates since random lists can overlap
      for i in header_sequence:
         if i in main_sequence:
            main_sequence.remove(i)

   decode_sequence = header_sequence + main_sequence

   decoded_data = ""
   # Read the bits from the file
   for i in range(0, embed_len):
      decoded_data += str(target_data[decode_sequence[i]] & 1)

   return decoded_data[header_len:] # don't return header


def lsb_embed(cover_data, target_data, header_len, key=""):
   """ Performs a Least Significant Bit embedding of a cover object

   Params:
      cover_data - List of bytes of the cover object
      target_data - String of bits that will be embedded into the cover object
      header_len - # of bits used to indicate hidden message length
      key - Password that determines the seed for the random num generator

   Returns:
      List of bytes represented as integers encoded using LSB 
   """ 
   embed_len = len(target_data)

   # Embed the header
   if key == "": # Sequentially
      header_sequence = range(0, header_len)
      main_sequence = range(len(header_sequence), embed_len)
   else: # Randomly
      random.seed(key)
      header_sequence = random.sample(range(0, len(cover_data)), header_len)
      main_sequence = random.sample(range(0, len(cover_data)), embed_len)
      # Remove duplicates since random lists can overlap
      for i in header_sequence:
         if i in main_sequence:
            main_sequence.remove(i)

   embed_sequence = header_sequence + main_sequence

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
