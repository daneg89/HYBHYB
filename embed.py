#!/usr/bin/python

from bit_manip import ascii_to_bits
from bpcs import bpcs_embed
from lsb import lsb_embed
from file_utils import calc_msg_header_len
from file_utils import create_header
from file_utils import get_file_name_from_path
from file_utils import get_file_type
from file_utils import file_to_bits
from PIL import Image
import constants
import image_utils
import sys

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
   except:
      print "Cover object type not recognized or missing. Provide a valid cover object!"
      exit()

   if cover_file_type == constants.IMAGE:
      embed_image(data["cover_obj"], data["target_obj"], data["key"], 
                  data["method"], data["show_image"], data["message"],
                  data["garbage"])
   else:
      print "Unsupported file type!"


def embed_image(cover_obj_path, target_obj_path, key, method, show_image,
                message, garbage):
   """ Function that handles image embedding

   Params:
      cover_obj_path - Path of the cover object   
      target_obj_path - Path of the target object   
      key - Key used to perform embedding (LSB only)
      method - Integer representing the embedding method
      show_image - Show the image after it's embedded?
      message - The plaintext message that will be embedded (if no target obj)
      garbage - Boolean that indicates if message should be generated or not

   """

   cover_obj = Image.open(cover_obj_path).copy() # Don't modify orig img
   color_depth = image_utils.get_color_depth(cover_obj.mode)
   message_bits = ""
   num_color_bands = image_utils.get_num_color_bands(cover_obj.mode)
   num_pixels = (cover_obj.size[0] * cover_obj.size[1]) # Width * Height
   num_embeddable_bits = (num_pixels * color_depth)

   # Calculate number of bits we can embed
   embed_capacity = est_embed_capacity(num_embeddable_bits, method)

   # Create the header
   header_len = calc_msg_header_len(num_embeddable_bits)

   if message != "": # Plaintext message
      message_bits = ascii_to_bits(message)
      plaintext_bit = "1"
   else: # File
      if garbage == True:
         fake_header = create_header(header_len, num_embeddable_bits)
         for i in range (0, (embed_capacity - (len(fake_header) + 1))):
            message_bits += str(i % 2)
      else:
         message_bits = file_to_bits(target_obj_path)

      plaintext_bit = "0"

   header_bits = create_header(header_len, len(message_bits))
   embed_data = header_bits + plaintext_bit + message_bits

   # Check bits > capacity
   if len(embed_data) > embed_capacity:
      print "Message exceeds length of target file!"
   else:
      if method == constants.BPCS:
         bpcs_embed(cover_obj, embed_data)
      else:
         # TODO: Get palette sorting to work with color gifs
         # Sort palette 
         if cover_obj.palette != None:
            image_utils.sort_palette(cover_obj)

         # Perform embedding
         cover_data = image_utils.image_to_bytes(cover_obj)
         embedded_data = lsb_embed(cover_data, embed_data, key)

         # Convert data back to format suitable for the cover type and write the file
         embedded_pixels = image_utils.bytes_to_pixels(
                           embedded_data, num_color_bands)


         cover_obj.putdata(embedded_pixels)

         steg_file_name = get_file_name_from_path(cover_obj_path)
         cover_obj.save(constants.PATH_STEGO + "Steg_" + steg_file_name)

def est_embed_capacity(num_bits, method):
   """ Estimates the embedding capacity of the specified object

   Params:
      num_bytes - The number of bits available for embedding
      method - The method used to embed the bytes

   """
   if method == constants.LSB:
      return num_bits / 8 # ~12.5%
   elif method == constants.BPCS:
      return int(num_bits * 0.3) # ~30%
   else:
      return 0
