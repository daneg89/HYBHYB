#!/usr/bin/python

def ascii_to_bits(ascii_str):
   """ Converts an ASCII String to bits

   Params:
      ascii_str - The ASCII String we want to convert

   Returns:
      String of bits (0s and 1s)

   """
   bit_string = ""

   for char in ascii_str:
      char_bits = bin(ord(char))[2:]
      if len(char_bits) < 7: # pad with 0's if necessary
         char_bits = "0" * (7 - len(char_bits)) + char_bits

      bit_string += char_bits

   return bit_string

def bit_from_byte(byte, bit_plane):
   """ Retrieves a bit from a byte located at the specified index

   Params:
      byte - The byte to get the bit from
      bit_plane - The index of the bit (0-7): 0 = MSB, 7 = LSB

   Returns:
      Integer of the bit: 0 or 1

   """
   # Subtract bit_plane from 7 to get the proper bit
   return (byte >> (7 - bit_plane)) & 1

def bits_to_ascii(bits):
   """ Converts a string of bits to ASCII text

   Params:
      bits - String of 0s and 1s representing an ASCII string

   Returns:
      String of ASCII characters

   """

   ascii_text = ""
   ch_size = 7 # Bit size of an ASCII CHunk

   # Organize bits into groups of 7
   ascii_chunks = [bits[i:i + ch_size] for i in range(0, len(bits), ch_size)]

   # Convert groups into characters and combine them
   for i in range(0, len(ascii_chunks)):
      ascii_text += chr(int(ascii_chunks[i], base=2))

   return ascii_text

def bits_to_bytes(bits):
   """ Converts a string of bits to a list of bytes
   
   Params:
      bits - String of 0s and 1s

   Returns:
      List of integers representing bytes
   
   """
   byte_size = 8
   byte_list = [bits[i:i + byte_size] for i in range(0, len(bits), byte_size)]
   return [int(i, 2) for i in byte_list]

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

def hex_to_bits(hex_string):
   """ Takes a hex_string and returns the bit representation of it """
   bit_string = str(bin(int(hex_string, base = 16))[2:]) # 0b will be sliced off
   bit_string_length = len(hex_string) * 4 # The real length of the bit string

   # We need the trailing zeros so make sure they are added here if missing
   num_lead_zeroes = bit_string_length - len(bit_string)

   return (("0" * num_lead_zeroes) + bit_string)

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
