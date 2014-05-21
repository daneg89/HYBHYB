#!/usr/bin/python

from bit_manip import bits_to_bytes
from bpcs import bpcs_embed
from lsb import lsb_embed
from file_utils import file_to_bits
import constants

def calc_embed_header(num_pixels, color_depth):
   """ Calculates the # of bits to use for a cover image's message length
   
   Params:
      num_pixels - Number of pixels in the Image
      color_depth - Number of bits that make up each color (8 or 24)
   
   """
   # TODO: implement
   pass

def est_embed_capacity(num_bits, method):
   """ Estimates the embedding capacity of the specified object

   Params:
      num_bytes - The number of bits to embed
      method - The method used to embed the bytes

   """
   if method == constants.LSB or method == constants.LSB_PR:
      return num_bits / 8 # ~12.5%
   elif method == constants.BPCS:
      return num_bits / 4 # 25%
   else:
      return 0


def embed_data(data):
   """ Generic embedding function that determines how to embed a file

   Params:
      data - Dictionary that carries the following information
         > "cover_obj": String
         > "target_obj": String
         > "key": String
         > "method": Int
         > "stats_mode": Bool
         > "show_image": Bool
         > "message": String
         > "garbage": Bool
   """
   # TODO: Get the data to embed

   # TODO: Calculate number of bits we can embed

   # TODO: Check bits > capacity


   # Test stub
   # Add the "1" for now to indicate that it's a plaintext message
   embed_data = "1" + file_to_bits(data["target_obj"])
   target_data = bits_to_bytes(file_to_bits(data["cover_obj"]))
   embedded_data = lsb_embed(target_data, embed_data)

def generate_message(embed_capacity):
   """

   Generates a random message for the purpose of testing the effectiveness
   of the program. Message will be about 98-99% of the embedding capacity
   that we specify.
 
   Params:
      embed_capacity - Number of bits that the target object can have modified

   """
   # TODO: implement
   pass
