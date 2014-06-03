#!/usr/bin/python

from bit_manip import cgc_to_pbc
from bit_manip import pbc_to_cgc
from image_utils import bytes_to_pixels
from image_utils import image_to_bytes
from image_utils import get_num_color_bands
import constants

def bpcs_embed(cover_image, data):
   """ Embeds a cover image using Bit-Plane Complexity Segmentation

   Params:
      cover_image - Image we want to hide our data in
      data - Collection of bits that will be embedded

   Note:
      Unlike lsb_embed, this function writes the embedded image instead
      of returning a set of embedded bits.

   """
   num_color_bands = get_num_color_bands(cover_image.mode)
   block_index = 0
   image_size = cover_image.size
   image_width = image_size[0]
   image_height = image_size[1]
   block_size = calc_block_size(image_size)
   bl_width = block_size[0]
   bl_height = block_size[1]
   cover_data = image_to_bytes(cover_image)

   # Convert image data to Canonical Gray Coding
   cgc_to_pbc(cover_data)
   cgc_pixels = bytes_to_pixels(cover_data, num_color_bands)

   # Embed ALL the data!
   while data != "":
      pixel_block = []
      y_pos = block_index / image_height
      # Get a block of pixels to embed
      # TODO: Verify that this works
      for y in range(y_pos, y_pos + bl_height):
         for x in range(block_index, block_index + bl_width):
            pixel_block.append(cgc_pixels[y * image_width + x])

      # Embed the pixel block

      # Increment block index
      block_index = get_next_block(block_index, bl_width, bl_height,
                                   image_width) 
      break # Temporarily here to prevent infinite loops



   # Convert image data back to Pure-Binary Coding
   pbc_to_cgc(cover_data)
   pixel_data = bytes_to_pixels(cover_data, num_color_bands)
   cover_image.putdata(pixel_data)


   # Save the embedded image
   cover_image.save(constants.PATH_STEGO + "BPCS_Steg.bmp")

def calc_block_size(image_size):
   """ Calculates message block size for embedding

   Params:
      image_size - (Width, Height) tuple of the image dimensions

   Returns:
      (Width, Height) of the message block

   """
   upper_limit = 11 # Prime numbers are always great for arbitrary bounds
   height = 0
   width = 0

   # Width
   for i in range(1, image_size[0] + 1):
      if image_size[0] % i == 0:
         width = i
      # Try to get biggest dimensions we can at or below the upper bound
      elif i > upper_limit and width > 0:
         break

   # Height
   for i in range(1, image_size[1]):
      if image_size[1] % i == 0:
         height = i
      elif i > upper_limit and height > 0:
         break

   return (width, height)

def get_next_block(curr_index, bl_width, bl_height, im_width):
   """ Increments the index so that we are at the position of the next block

   Params:
      curr_index - The current index
      bl_width - The width of the message block
      bl_height - The height of the message block
      im_width - The width of the image block

   Returns:
      Index of the top left corner of the next block
   
   """
   num_width_blocks = im_width / bl_width
   new_index = curr_index + 1 # Make the index 1-based for modulus operations

   # If we are at the end of the "row", drop down a couple "rows" and
   if (new_index + (bl_width - 1)) % (num_width_blocks * bl_width) == 0:
      new_index += (((bl_height - 1) * im_width) + 
                   (im_width - (bl_width * num_width_blocks)))
   
   # Always increment by at least the block's width
   new_index += bl_width
   return new_index - 1 # Back to 0-based indices
