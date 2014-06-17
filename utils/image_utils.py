#!/usr/bin/python

from PIL import Image

def bnw_palette(img_palette):
   """ Changes an image's palette so that the colors are black and white

   Params:
      img_palette - List of 768 integers (3 colors for 256 palette colors)
   """

   # Alternate between black and white
   for i in range(0, len(img_palette), 3):
      if i % 2 == 0: # Black
         img_palette[i] = 0
         img_palette[i + 1] = 0
         img_palette[i + 2] = 0
      else: # White
         img_palette[i] = 255
         img_palette[i + 1] = 255
         img_palette[i + 2] = 255

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

def image_to_bytes(image):
   """ Converts an Image to its byte representation
   
   Params:
      image - The Image we want to convert to bytes

   Returns:
      List of integers representing bytes of the image 

   """
   pixel_data = list(image.getdata())
   return pixels_to_bytes(pixel_data)

def is_grayscale(image):
   """ Checks to see if an image is grayscale or not

   Params:
      image - The Image we are checking

   Returns:
      True or False

   """

   palette = image.getpalette()
   is_grayscale = True

   # Go over half the pixels and see if the RGB values match
   for i in range(0, len(palette) / 2, 3):
      if palette[i] != palette[i + 1] and palette[i] != palette[i + 2]:
         is_grayscale = False

   return is_grayscale

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

   if is_grayscale(palette_image): # Grayscale sorted normally
      new_palette.sort()
   else: # Color sorted by luminosity
      new_palette = sorted(new_palette, key=sum) # Sort by pixel luminosity

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
