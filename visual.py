#!/usr/bin/python

from bit_manip import bit_from_byte
from file_utils import get_file_name_from_path
from image_utils import bnw_palette
from image_utils import bytes_to_pixels
from image_utils import get_num_color_bands
from image_utils import image_to_bytes
from PIL import Image
import constants

def filtered_visual_attack(img_path):
   """ Performs a filtered visual attack against an image

   Params:
      img_path - Path to a palette image

   Notes:
      Writes the visually attacked image to the "steganalysis" dir
      Use this ONLY with palette images, otherwise will not work as expected

   """
   # Get file name so we can save it later
   img_name = get_file_name_from_path(img_path)

   # Open the image and get the palette
   original_img = Image.open(img_path).copy()
   original_palette = original_img.getpalette()

   # Modify the palette
   bnw_palette(original_palette)
   original_img.putpalette(original_palette)

   original_img.save(constants.PATH_STEGA + "FVis_" + img_name)

def visual_attack(img_path):
   """ Performs a visual attack against an image

   Params:
      img_path - Path to an image

   Notes:
      Writes both visually attacked image to the "steganalysis" dir
      Do NOT use this with palette images, will not work as expected

   """
   # Get file name so we can save them later
   img_name = get_file_name_from_path(img_path)

   # Open the image
   original_img = Image.open(img_path).copy()

   # Get the image pixel values
   original_data = image_to_bytes(original_img)

   # Show all LSB changes by modifying colors based on the LSB
   for i in range(0, len(original_data), 3):
      lsb = bit_from_byte(original_data[i], 7)
      if lsb == 0:
         original_data[i] = 0
         original_data[i + 1] = 0
         original_data[i + 2] = 0
      else:
         original_data[i] = 255
         original_data[i + 1] = 255
         original_data[i + 2] = 255

   num_colors = get_num_color_bands(original_img.mode)
   new_pixels = bytes_to_pixels(original_data, num_colors)
   original_img.putdata(new_pixels)

   # Save the image
   original_img.save(constants.PATH_STEGA + "Vis_" + img_name)
