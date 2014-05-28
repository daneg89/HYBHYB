#!/usr/bin/python

from bit_manip import bits_to_bytes
from file_utils import calc_msg_header_len
from file_utils import create_header
from file_utils import get_file_type
from file_utils import file_to_bits
from image_utils import get_color_depth
from image_utils import pixels_to_bytes
from lsb import lsb_decode
from PIL import Image
import constants

def decode_data(data):
   """ Generic decoding function that determines how to decode a file

   Params:
      data - Dictionary that carries the following information
         > "cover_obj": String (Not needed for decoding)
         > "target_obj": String
         > "key": String
         > "method": Int
         > "stats_mode": Bool (Not needed for decoding)
         > "show_image": Bool (Not needed for decoding)
         > "message": String (Not needed for decoding)
         > "garbage": Bool (Not needed for decoding)
   """
   # Get the file to decode
   try:
      target_file_type = get_file_type(data["target_obj"])
   except: # TODO: Catch the exception
      pass

   if target_file_type == constants.IMAGE:
      decode_image(data["target_obj"], data["key"], data["method"]) 
   else:
      print "Unsupported file type!"
   
def decode_image(target_obj_path, key, method):
   """ Takes a stego-image and decodes the message inside it

   Params:
      target_obj_path - Path of the object to decode
      key - LSB only, determines sequence of decoding
      method - Integer representing what method to use to decode the file

   """

   # Get image data
   target_obj = Image.open(target_obj_path).copy() # Don't modify orig img
   color_depth = get_color_depth(target_obj.mode)
   num_pixels = (target_obj.size[0] * target_obj.size[1]) # Width * Height

   # Calculate header length
   header_len = calc_msg_header_len(num_pixels * color_depth)

   # Get the data from the image
   pixel_data = list(target_obj.getdata())
   target_data = pixels_to_bytes(pixel_data)

   if method == constants.BPCS:
      pass
   else:
      decode_results = lsb_decode(target_data, header_len, key)
      plaintext_bit = decode_results[0:1]

      if plaintext_bit == "0":
         is_plaintext = False
      else:
         is_plaintext = True

   write_result(decode_results[1:], False)


def write_result(data, is_plaintext):
   """ Takes the results of the decoding and writes them out

   Params:
      data - String of bits that make up the decoded message
      is_plaintext - Is it a plaintext message or a binary file?

   """

   if is_plaintext == True:
      # TODO: Convert data to ASCII
      print "something"
   else:
      # Convert data to bytearray
      write_data = bytearray(bits_to_bytes(data))

      # TODO: Generate filename

      # Write file
      new_file = open(constants.PATH_EXTRACT + "Extract_001", "wb")
      new_file.write(write_data)
      new_file.close()
