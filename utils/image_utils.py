#!/usr/bin/python

def bytes_to_pixels(byte_list, color_depth):
   """

   """
   pass

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

def pixels_to_bytes(pixel_list):
   """ Converts a list of pixels (set of tuples) to a list of bytes

   Params:
      pixel_list - list of pixel tuples to convert

   Returns:
      List of integers representing bytes

   """
   return [byte for tup in pixel_list for byte in tup]
