#!/usr/bin/python

from bit_manip import cgc_to_pbc
from bit_manip import bit_from_byte
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

   # Need pixels formatted as lists instead of tuples so they can be changed
   cgc_pixels = [cover_data[i:i + num_color_bands] 
                for i in range(0, len(cover_data), num_color_bands)]

   # Embed ALL the data!
   while data != "":
      pixel_block = []
      # Get a block of pixels to embed
      for y in range(0, bl_height):
         for x in range(block_index, block_index + bl_width):
            pixel_block.append(cgc_pixels[y * image_width + x])

      # Embed the pixel block
      embed_block(pixel_block, data, bl_width, bl_height)

      # Update pixels to reflect embedding
      pblock_y = 0

      for y in range(0, bl_height):
         pblock_x = 0
         for x in range(block_index, block_index + bl_width):
            cgc_pixels[y * image_width + x] = pixel_block[pblock_y * bl_width + pblock_x]
            pblock_x += 1
         pblock_y += 1

      # Increment block index
      block_index = get_next_block(block_index, bl_width, bl_height,
                                   image_width) 
      break # Temporarily here to prevent infinite loops

   # Flatten the CGC Pixels and use them for embedding the image
   cover_data = [byte for pixel in cgc_pixels for byte in pixel]

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
   for i in range(1, image_size[0]):
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

def get_color_block_complexity(block, color, bit_plane, bl_width, bl_height):
   """ Calculates a color's complexity for BPCS embedding purposes
   
   Params:
      block - A list of lists representing pixels (each sublist has 3 elements)
      color - Integer, Red = 0, Green = 1, Blue = 2
      bit_plane - Integer from 0 to 7, 0 = MSB, 7 = LSB
      bl_width - Width of the block we are checking
      bl_height - Height of the block we are checking

   Returns:
      
   """
   # TODO: Verify that this function works
   complexity = 0.0
   num_bit_changes = 0
   total_bit_changes = 0
   total_header_len = 0

   # Calculate complexity from left to right
   for y in range(0, bl_height):
      for x in range(0, bl_width):
         # Stop if at the end
         if (y == bl_height - 1 and x == bl_width - 1):
            total_bit_changes += num_bit_changes
            break
         else:
            curr_pos = y * bl_width + x
            curr_bit = bit_from_byte(block[curr_pos][color], bit_plane)
            next_bit = bit_from_byte(block[curr_pos + 1][color], bit_plane)
            if next_bit == curr_bit:
               # Need to calculate total number of color changes in the block
               if num_bit_changes > 0:
                  total_header_len += num_bit_changes
               total_bit_changes += num_bit_changes
               num_bit_changes = 0
            else:
               num_bit_changes += 1

   num_bit_changes = 0

   # Calculate complexity from top to bottom
   for x in range(0, bl_width):
      for y in range(0, bl_height):
         # Stop if at the end
         if (y == bl_height - 1 and x == bl_width - 1):
            total_bit_changes += num_bit_changes
            break
         else:
            curr_pos = y * bl_width + x
            curr_bit = bit_from_byte(block[curr_pos][color], bit_plane)
            next_bit = bit_from_byte(block[curr_pos + 1][color], bit_plane)
            if next_bit == curr_bit:
               # Need to calculate total number of color changes in the block
               if num_bit_changes > 0:
                  total_header_len += num_bit_changes
               total_bit_changes += num_bit_changes
               num_bit_changes = 0
            else:
               num_bit_changes += 1

   # Add 1 since loops didn't cover last bit of the image
   total_bit_changes += 1

   return float(total_header_len) / total_bit_changes


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

def embed_bit_plane(block, color, bit_plane, data):
   """


   """

   # Test code

   pass

def embed_block(block, data, bl_width, bl_height):
   """ Embeds a pixel block BPCS-style by modifying the block in place

   Params:
      block - A list of lists representing pixels (each sublist has 3 elements)
      data - String of 0s and 1s to be embedded
      bl_width - Width of the block we are embedding
      bl_height - Height of the block we are embedding

   """
   bit_plane = 7 # Start at LSB
   color = 0
   threshold = 0.4 # Threshold for how complex a block is; bigger = complex
   num_colors = 3 # RGB

   # Determine complexity of the message, conjugate if necessary


   while True:
      if bit_plane >= 0:
         complexity = get_color_block_complexity(block, color, bit_plane,
                                                 bl_width, bl_height)

      if complexity <= threshold or bit_plane < 0:
         color += 1
         bit_plane = 7
         if color == num_colors:
            break
      else:
         # Test Code
         for y in range(0, bl_height):
            for x in range(0, bl_width):
               target = y * bl_width + x
               embed_bit_plane(block[target], color, bit_plane, data)
         bit_plane -= 1
