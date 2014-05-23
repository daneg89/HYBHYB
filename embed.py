#!/usr/bin/python

import sys

from bit_manip import bits_to_bytes
from bpcs import bpcs_embed
from lsb import lsb_embed
from file_utils import get_file_type
from file_utils import file_to_bits
from PIL import Image
import constants
import image_utils
import math

def calc_msg_header_len(num_embeddable_bits):
   """ Calculates the # of bits to use for a cover object's message length
   
   Params:
      num_embeddable_bits - Number of bits that we can actually use for embedding
   
   """
   return int(math.ceil(math.log(num_embeddable_bits, 2)))

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
   try:
      cover_file_type = get_file_type(data["cover_obj"])
   except: # TODO: Catch the exception
      pass

   if cover_file_type == constants.IMAGE:
      cover_obj = Image.open(data["cover_obj"]).copy() # Don't modify orig img
      color_depth = image_utils.get_color_depth(cover_obj.mode)
      num_pixels = (cover_obj.size[0] * cover_obj.size[1]) # Width * Height
      pixel_data = list(cover_obj.getdata())
      cover_data = image_utils.pixels_to_bytes(pixel_data)
      num_embeddable_bits = (num_pixels * color_depth)
   else:
      print "Unsupported file type!"

   # Create the header
   header_len = calc_msg_header_len(num_embeddable_bits)
   header_bits = create_header(header_len, len(data))

   # Add the "1" for now to indicate that it's a plaintext message
   plaintext_bit = "1" # Stub code
   embed_data = plaintext_bit + header_bits + file_to_bits(data["target_obj"])

   # Calculate number of bits we can embed
   embed_capacity = est_embed_capacity(len(embed_data), data["method"])

   # TODO: Check bits > capacity


   # TODO: Determine what embedding to do and perform it
   embedded_data = lsb_embed(cover_data, embed_data)

   # Convert data back to format suitable for the cover type and write the file
   if cover_file_type == constants.IMAGE:
      num_color_bands = image_utils.get_num_color_bands(cover_obj.mode)
      embedded_pixels = image_utils.bytes_to_pixels(
                        embedded_data, num_color_bands)
      cover_obj.putdata(embedded_pixels)
      cover_obj.save(constants.STEGO + "Steg_" + "001.jpg")
   else:
      pass

   # TODO: Write the stego object

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
