#!/usr/bin/python

def bits_to_bytes(bits):
   """ Converts a string of bits to bytes 
   
   Params:
      bits - String of 0s and 1s

   Returns:
      List of bytes
   
   """
   return bits # Test code, TODO: implement

def hex_to_bits(hex_string):
   """ Takes a hex_string and returns the bit representation of it """
   bit_string = str(bin(int(hex_string, base = 16))[2:]) # 0b will be sliced off
   bit_string_length = len(hex_string) * 4 # The real length of the bit string

   # We need the trailing zeros so make sure they are added here if missing
   num_lead_zeroes = bit_string_length - len(bit_string)

   return (("0" * num_lead_zeroes) + bit_string)

def tuples_to_bits(tuples):
   """ Converts a list of tuples to bits
   
   Params:
      tuples - List of tuples
   
   """
   bit_string = ""

   # TODO: make sure 0 bits added in front

   # TODO: fix this, probably implement a different way
   for tup in tuples:
      for x in tup:
         bit_string += bin(tup[x])[2:] # 0b will be sliced off

   return bit_string
