#!/usr/bin/python

from bit_manip import cgc_to_pbc
from bit_manip import bit_from_byte
from bit_manip import pbc_to_cgc
from image_utils import bytes_to_pixels
from image_utils import image_to_bytes
from image_utils import get_num_color_bands
import constants

def bpcs_decode(stego_data, image_size, header_len):
   """ Decodes a stego-image that was embedded using BPCS

   Params:
      stego_data - List of bytes representing pixels of the image
      image_size - Tuple that contains data (Width, Height) of the image
      header_len - # of bits used to indicate hidden message length

   Returns:
      String of 0s and 1s representing the decoded data

   """
   bits_read = 0
   block_index = 0
   block_size = calc_block_size(image_size)
   bl_width = block_size[0]
   bl_height = block_size[1]
   decoded_data = ""
   image_width = image_size[0]
   image_height = image_size[1]
   num_color_bands = 3

   # Convert image data to Canonical Gray Coding
   cgc_to_pbc(stego_data)

   # Pixel formatting
   cgc_pixels = [stego_data[i:i + num_color_bands]
                for i in range(0, len(stego_data), num_color_bands)]

   # Read the header bits
   while len(decoded_data) < header_len:
      pixel_block = []
      # Get a block of pixels to decode
      for y in range(0, bl_height):
         for x in range(block_index, block_index + bl_width):
            pixel_block.append(cgc_pixels[y * image_width + x])


      # Decode pixels
      decoded_data += decode_block(pixel_block, bl_width, bl_height)

      # Increment block index
      block_index = get_next_block(block_index, bl_width, bl_height,
                                   image_width)

   # Get message length, shave off header bits
   # +1 to account for plaintext bit
   decode_len = int(decoded_data[0:header_len], base=2) + 1
   decoded_data = decoded_data[header_len:]

   # Decode ALL the data!
   while len(decoded_data) < decode_len:
      pixel_block = []
      for y in range(0, bl_height):
         for x in range(block_index, block_index + bl_width):
            pixel_block.append(cgc_pixels[y * image_width + x])

      decoded_data += decode_block(pixel_block, bl_width, bl_height)

      block_index = get_next_block(block_index, bl_width, bl_height,
                                   image_width)

   # Truncate any extra bits if necessary
   if len(decoded_data) > decode_len:
      decoded_data = decoded_data[0:decode_len]

   return decoded_data

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

   # Subtract 1 since each block will have a conjugation bit added
   message_len = (bl_width * bl_height) - 1

   # Convert the data into a blocky format
   data = [data[i:i + message_len] for i in range(0, len(data), message_len)]
   if len(data[-1]) < (message_len + 1): # Pad the last value with 1s and 0s
      for i in range(0, (message_len) - len(data[-1])):
         data[-1] = data[-1] + bin(i % 2)[2:]
         
   # Add the conjugation bits to all the blocks
   for i in range(0, len(data)):
      data[i] = "0" + data[i]

   # Flatten data
   data = [bit for bit_string in data for bit in bit_string]

   # Embed ALL the data!
   while data != []:
      pixel_block = []

      # Get a block of pixels to embed
      for y in range(0, bl_height):
         for x in range(block_index, block_index + bl_width):
            pixel_block.append(cgc_pixels[y * image_width + x])

      # Embed the pixel block
      bits_embedded = embed_block(pixel_block, data, bl_width, bl_height)

      # Shorten the data so we don't have to copy it over to a new list
      if bits_embedded >= len(data):
         data = []
      else:
         del data[0:bits_embedded]

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

def conjugate_block(data, bl_width, bl_height):
   """ Conjugates a block so that it is more suitable to embed
   Params:
      data - String of 0s and 1s to be conjugated
      bl_width - The width of the message block
      bl_height - The height of the message block

   Returns:
      String of conjugated 1s and 0s

   """
   conjugated_block = "1" # First bit indicates the block is conjugated

   # The "white checkerboard" is used to xor bits of the original message
   # to create the conjugated version of the message. First bit is white (0),
   # then black (1), white (0), and so on
   white_checkerboard = gen_white_checkerboard(bl_width, bl_height)

   for y in range(0, bl_height):
      for x in range(0, bl_width):
         if x == 0 and y == 0:
            continue
         else:
            curr_pos = y * bl_width + x
            data_bit = int(data[curr_pos], base=2)
            board_bit = int(white_checkerboard[curr_pos], base=2)
            conjugated_block += str(data_bit ^ board_bit)

   return conjugated_block

def decode_bit_plane(block, color, bit_plane):
   """ Decodes a bit plane of a single pixel and single color

   Params:
      block - List of 3 RGB integers
      color - The index for the block of which color will be changed
      bit_plane - Integer from 0 to 7, 0 = MSB, 7 = LSB

   """

   return str(bit_from_byte(block[color], bit_plane))

def decode_block(block, bl_width, bl_height):
   """ Decodes a pixel block BPCS-style

   Params:
      block - A list of lists representing pixels (each sublist has 3 elements)
      bl_width - Width of the block we are decoding
      bl_height - Height of the block we are decoding

   Returns:
      String of decoded 0s and 1s

   """
   bits_decoded = ""
   bit_plane = 7 # Start at LSB
   color = 0
   conjugation_offset = 0
   num_colors = 3 # RGB

   while True:
      if bit_plane >= 0:
         # Set the conjugation bits temporarily to 0 to get the 
         # "true" complexity
         for i in range(0, bit_plane):
            if bit_from_byte(block[0][color], i) == 1:
               conjugation_offset += 1 << (7 - i)

         block[0][color] -= conjugation_offset
         complexity = get_color_block_complexity(block, color, bit_plane,
                                                 bl_width, bl_height)
         # Restore conjugation bits
         block[0][color] += conjugation_offset
         conjugation_offset = 0

      if complexity < get_threshold(bit_plane) or bit_plane < 0:
         color += 1
         bit_plane = 7
         if color == num_colors: # Ran out of colors
            break
      else:
         # Decode the block
         block_bits = ""
         for y in range(0, bl_height):
            for x in range(0, bl_width):
               target = y * bl_width + x
               block_bits += decode_bit_plane(block[target], color, bit_plane)

         # Deconjugate blocks as needed
         if block_bits[0] == "1":
            block_bits = deconjugate_block(block_bits, bl_width, bl_height)
         else:
            # Need to strip the conjugation bit or causes problems
            block_bits = block_bits[1:]
            
         bits_decoded += block_bits
         bit_plane -= 1

   return bits_decoded

def deconjugate_block(data, bl_width, bl_height):
   """ Deconjugates a conjugated block
   Params:
      data - String of 0s and 1s to be deconjugated
      bl_width - The width of the message block
      bl_height - The height of the message block

   Returns:
      String of deconjugated 1s and 0s

   """
   dec_bits = ""
   white_checkerboard = gen_white_checkerboard(bl_width, bl_height)

   # Start from 1 to strip the conjugation bit
   for i in range(1, len(data)):
      if data[i] == white_checkerboard[i]:
         dec_bits += "0"
      else:
         dec_bits += "1"

   return dec_bits

def get_color_block_complexity(block, color, bit_plane, bl_width, bl_height):
   """ Calculates a color's complexity for BPCS embedding purposes
   Params:
      block - A list of lists representing pixels (each sublist has 3 elements)
      color - Integer, Red = 0, Green = 1, Blue = 2
      bit_plane - Integer from 0 to 7, 0 = MSB, 7 = LSB
      bl_width - Width of the block we are checking
      bl_height - Height of the block we are checking

   Returns:
      Floating point number x where 0.0 <= x <= 1.0
   """
   max_num_changes = get_max_num_changes(bl_width, bl_height)

   # Get the values from the block that we need
   main_block = [bcolor[color] for bcolor in block]

   l_to_r_complexity = left_to_right_complexity(main_block, bit_plane,
                                                bl_width, bl_height)
   t_to_b_complexity = top_to_bottom_complexity(main_block, bit_plane,
                                                bl_width, bl_height)

   total_complexity = l_to_r_complexity + t_to_b_complexity

   return float(total_complexity) / max_num_changes

def get_msg_block_complexity(block, bl_width, bl_height):
   """ Calculates a message block's complexity
   Params:
      block - A string of 0s and 1s
      bl_width - Width of the block we are checking
      bl_height - Height of the block we are checking

   """
   bit_plane = 7
   max_num_changes = get_max_num_changes(bl_width, bl_height)

   # Convert the data to a format compatible with the complexity calculator
   main_block = [int(bit) for bit in block]

   l_to_r_complexity = left_to_right_complexity(main_block, bit_plane,
                                                bl_width, bl_height)
   t_to_b_complexity = top_to_bottom_complexity(main_block, bit_plane,
                                                bl_width, bl_height)

   total_complexity = l_to_r_complexity + t_to_b_complexity

   return float(total_complexity) / max_num_changes

def get_max_num_changes(bl_width, bl_height):
   """ Function to determine the max number of changes possible in a block
   Params:
      bl_width - The width of the block
      bl_height - The height of the block

   """
   bit_plane = 7
   board = [int(bit) for bit in gen_white_checkerboard(bl_width, bl_height)]

   l_to_r_changes = left_to_right_complexity(board, bit_plane, 
                                             bl_width, bl_height)
   t_to_b_changes = top_to_bottom_complexity(board, bit_plane, 
                                             bl_width, bl_height)

   return (l_to_r_changes + t_to_b_changes)

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

   # If we are at the end of the "row", drop down a couple "rows"
   if (new_index + (bl_width - 1)) % (num_width_blocks * bl_width) == 0:
      new_index += (((bl_height - 1) * im_width) +
                   (im_width - (bl_width * num_width_blocks)))
   
   # Always increment by at least the block's width
   new_index += bl_width
   return new_index - 1 # Back to 0-based indices

def get_threshold(bit_plane):
   """ Dynamically determines BPCS threshold based on the bit plane

   Params:
      bit_plane - The bit plane that will be embedded

   Returns:
      Float that corresponds to the complexity threshold

   """
   if bit_plane == 7:
      threshold = 0.0 # Always embed LSB
   elif bit_plane == 6:
      threshold = 0.2
   elif bit_plane == 5:
      threshold = 0.3
   else:
      threshold = 0.45

   return threshold

def gen_white_checkerboard(bl_width, bl_height):
   """ Generates a white checkerboard

   Params:
      bl_width - The width of the board
      bl_height - The height of the board

   Returns:
      String of alternating 0s and 1s

"""
   white_checkerboard = ""

   for i in range(0, (bl_width * bl_height)):
      white_checkerboard += bin(i % 2)[2:]

   return white_checkerboard

def embed_bit_plane(block, color, bit_plane, data):
   """ Embeds a bit plane of a single pixel and single color

   Params:
      block - List of 3 RGB integers
      color - The index for the block of which color will be changed
      bit_plane - Integer from 0 to 7, 0 = MSB, 7 = LSB
      data - String of a 1 or 0 to be embedded

   """
   block_bit = bit_from_byte(block[color], bit_plane)
   new_bit = int(data, base=2)
   bit_distance = 7 - bit_plane
   bit_val = 1 << bit_distance

   if block_bit > new_bit:
      block[color] -= bit_val
   elif block_bit < new_bit:
      block[color] += bit_val
   else:
      pass

def embed_block(block, data, bl_width, bl_height):
   """ Embeds a pixel block BPCS-style by modifying the block in place

   Params:
      block - A list of lists representing pixels (each sublist has 3 elements)
      data - String of 0s and 1s to be embedded
      bl_width - Width of the block we are embedding
      bl_height - Height of the block we are embedding

   Returns:
      Number of bits embedded in the block

   """
   bits_embedded = 0
   bit_plane = 7 # Start at LSB
   color = 0
   lsb = 7
   num_colors = 3 # RGB

   while True:
      if bit_plane >= 0:
         complexity = get_color_block_complexity(block, color, bit_plane,
                                                 bl_width, bl_height)
      if complexity < get_threshold(bit_plane) or bit_plane < 0:
         color += 1
         bit_plane = 7
         if color == num_colors: # Ran out of colors
            break
      else:
         message = data[bits_embedded:(bits_embedded + (bl_width * bl_height))]
         if message == []:
            break

         # Conjugate message as needed
         block_complexity = get_msg_block_complexity(message, bl_width, bl_height)
         if block_complexity < get_threshold(bit_plane):
            message = conjugate_block(message, bl_width, bl_height)

         for y in range(0, bl_height):
            for x in range(0, bl_width):
               target = y * bl_width + x
               if bits_embedded >= len(data): # Embedded all the bits we can
                  break
               else:
                  embed_bit_plane(block[target], color, bit_plane,
                                  message[bits_embedded % len(message)])
                  bits_embedded += 1
         bit_plane -= 1

   return bits_embedded

def left_to_right_complexity(block, bit_plane, bl_width, bl_height):
   """ Gets the complexity of a block from left to right

   Params:
      block - List of integers
      bit_plane - Which plane to focus on
      bl_width - Width of the block we are checking
      bl_height - Height of the block we are checking

   Returns:
      Float representing complexity of the block from left to right

   """

   num_bit_changes = 0
   total_header_len = 0

   for y in range(0, bl_height):
      for x in range(0, bl_width):
         # Stop if at the end
         if (y == bl_height - 1 and x == bl_width - 1):
            total_header_len += num_bit_changes
            break
         else:
            curr_pos = y * bl_width + x
            curr_bit = bit_from_byte(block[curr_pos], bit_plane)
            next_bit = bit_from_byte(block[curr_pos + 1], bit_plane)
            if next_bit == curr_bit:
               # Calculate total number of color changes in the block
               total_header_len += num_bit_changes
               num_bit_changes = 0
            else:
               num_bit_changes += 1

   return total_header_len

def top_to_bottom_complexity(block, bit_plane, bl_width, bl_height):
   """ Gets the complexity of a block from top to bottom

   Params:
      block - List of integers
      bit_plane - Which plane to focus on
      bl_width - Width of the block we are checking
      bl_height - Height of the block we are checking

   Returns:
      Float representing complexity of the block from top to bottom

   """

   num_bit_changes = 0
   total_header_len = 0

   for x in range(0, bl_width):
      for y in range(0, bl_height):
         # Stop if at the end
         if (y == bl_height - 1 and x == bl_width - 1):
            total_header_len += num_bit_changes
            break
         else:
            curr_pos = y * bl_width + x
            curr_bit = bit_from_byte(block[curr_pos], bit_plane)
            next_bit = bit_from_byte(block[curr_pos + 1], bit_plane)
            if next_bit == curr_bit:
               # Calculate total number of color changes in the block
               total_header_len += num_bit_changes
               num_bit_changes = 0
            else:
               num_bit_changes += 1

   return total_header_len
