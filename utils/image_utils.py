#!/usr/bin/python

def bytes_to_pixels(byte_list, num_color_bands):
   """ Takes an array of integers and coverts it into pixel format (tuples)

   Params:
      byte_list - List of integers used for pixel values
      num_color_bands - Number of values in pixel tuple (Usually 1 or 3)

   Returns:
      List of tuples representing pixels

   """
   if num_color_bands > 1:
      pixel_list = [tuple(byte_list[i:i + num_color_bands]) for i in range(
                    0, len(byte_list), num_color_bands)]
   else:
      pixel_list = byte_list # Don't format as tuples, just return list

   return pixel_list

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
   """ Converts a list of pixels to a list of bytes

   Params:
      pixel_list - list of pixels to convert

   Returns:
      List of integers representing bytes

   Note:
      Depending on the image type, the list may either be a list of tuples or
      a list of integers. 

   """
   if type(pixel_list[0]) == type(tuple()):
      byte_list = [byte for tup in pixel_list for byte in tup]
   else:
      byte_list = pixel_list

   return byte_list

def sort_palette(palette):
   """ Parses and sorts a palette
   
   Params:
      palette - Object returned from Image.getpalette()

   Returns:
      A list of 768 integers for a new sorted palette

   """
   new_palette = [palette[i:i + 3] for i in range(0, len(palette), 3)]
   new_palette.sort()
   new_palette = [palette_val for sublist in new_palette for palette_val in sublist]
   return new_palette
