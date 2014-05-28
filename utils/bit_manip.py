#!/usr/bin/python

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

def hex_to_bits(hex_string):
   """ Takes a hex_string and returns the bit representation of it """
   bit_string = str(bin(int(hex_string, base = 16))[2:]) # 0b will be sliced off
   bit_string_length = len(hex_string) * 4 # The real length of the bit string

   # We need the trailing zeros so make sure they are added here if missing
   num_lead_zeroes = bit_string_length - len(bit_string)

   return (("0" * num_lead_zeroes) + bit_string)

def ascii_to_bits(ascii_str):
   """ Converts an ASCII String to bits

   Params:
      ascii_str - The ASCII String we want to convert

   Returns:
      String of bits (0s and 1s)

   """
   bit_string = ""

   for char in ascii_str:
      bit_string += bin(ord(char))[2:]

   return bit_string
