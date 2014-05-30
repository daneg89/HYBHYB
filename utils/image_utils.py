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

def cgc_to_pbc(byte_list):
   """ Converts a set of bytes from Canonical Gray Coding to Pure-Binary Coding 

   Params:
      byte_list - List of integers representing bytes

   See http://www.datahide.com/BPCSe/pbc-vs-cgc-e.html for more information
   on converting between CGC and PBC

   """
   gray_bytes = gen_cgc_table()

   for i in range(0, len(byte_list)):
      byte_list[i] = gray_bytes.index(byte_list[i])

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

def gen_cgc_table(as_bytes=True):
   """ Generates a CGC table
   Params:
      as_bytes - Return the table as a list of bytes (Integers) or 
                 bits (Strings)
   
   Returns:
      List of Integers or Strings formatted according to CGC

   """
   byte_len = 8
   byte_size = 256

   # Create list of CGC values
   # MSBs only for the gray bytes 
   gray_bytes = [bin(x/(byte_size / 2))[2:] for x in range(0, byte_size)] 
   pure_bytes = [bin(x)[2:] for x in range(0, byte_size)]

   # Create the conversion list
   for byte in range(0, byte_size):
      # Pad pbc list with 0s if necessary
      if len(pure_bytes[byte]) < byte_len:
         num_zeroes = byte_len - len(pure_bytes[byte])
         pure_bytes[byte] = ('0' * num_zeroes) + pure_bytes[byte]
      # Start from 1 since the MSB is identical
      for bit in range(1, len(pure_bytes[byte])):
         gray_bytes[byte] += str(int(pure_bytes[byte][bit - 1], base=2) ^ 
                                 int(pure_bytes[byte][bit], base=2))

   # Determine table formatting
   if as_bytes == True:
      for i in range(0, len(gray_bytes)):
         gray_bytes[i] = int(gray_bytes[i], base=2)

   return gray_bytes

def pbc_to_cgc(byte_list):
   """ Converts a set of bytes from Pure-Binary Coding to Canonical Gray Coding
   Params:
      byte_list - List of integers representing bytes

   See http://www.datahide.com/BPCSe/pbc-vs-cgc-e.html for more information
   on converting between PBC and CGC

   """
   gray_bytes = gen_cgc_table()

   # Convert our given bytes to CGC
   for i in range(0, len(byte_list)):
      byte_list[i] = gray_bytes[byte_list[i]]

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

def sort_palette(palette_image):
   """ Parses and sorts the palette of an image
   
   Params:
      palette_image - Image that has a palette

   """
   old_palette = palette_image.getpalette()
   # Create a new palette that we can sort
   new_palette = [old_palette[i:i + 3] for i in range(0, len(old_palette), 3)]
   new_palette.sort()
   old_palette = [old_palette[i:i + 3] for i in range(0, len(old_palette), 3)]

   # Create the pixel map
   pixel_map = {k:v for k in range(0, len(old_palette)) for v in new_palette}
   for i in range(len(old_palette)):
      pixel_map[i] = old_palette[i]

   # Map pixels to new palette
   pixel_list = pixels_to_bytes(list(palette_image.getdata()))

   for i in range(len(pixel_list)):
      pixel_list[i] = new_palette.index(pixel_map[pixel_list[i]])

   palette_image.putdata(pixel_list)

   # Create one contiguous palette
   new_palette = [palette_val for sublist in new_palette for palette_val in sublist]
   palette_image.putpalette(new_palette)
