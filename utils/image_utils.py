#!/usr/bin/python

def bytes_to_pixels(byte_list, num_color_bands):
   """ Takes an array of integers and coverts it into pixel format (tuples)

   Params:
      byte_list - List of integers used for pixel values
      num_color_bands - Number of values in pixel tuple (Usually 1 or 3)

   Returns:
      List of tuples representing pixels

   """

   return [tuple(byte_list[i:i + num_color_bands]) for i in range(
          0, len(byte_list), num_color_bands)]

def get_color_depth(mode):
   """ Gets the color depth based on the Image mode 
   
   Params:
      mode - String representing the Image's mode 

   See http://pillow.readthedocs.org/en/latest/handbook/concepts.html for
   more information on mode types
   
   """

   if mode == "L" or mode == "P":
      return 8
   elif mode == "RGB":
      return 24
   else:
      print "Unsupported image mode given!"
      return 1

def get_num_color_bands(mode):
   """ Gets the number of color bands based on the Image mode 
   
   Params:
      mode - String representing the Image's mode 

   See http://pillow.readthedocs.org/en/latest/handbook/concepts.html for
   more information on mode types
   
   """

   if mode == "L" or mode == "P":
      return 1
   elif mode == "RGB":
      return 3
   else:
      print "Unsupported image mode given!"
      return 1

def pixels_to_bytes(pixel_list):
   """ Converts a list of pixels (set of tuples) to a list of bytes

   Params:
      pixel_list - list of pixel tuples to convert

   Returns:
      List of integers representing bytes

   """
   return [byte for tup in pixel_list for byte in tup]
