#!/usr/bin/python

def hex_to_bits(hex_string):
   """ Takes a hex_string and returns the bit representation of it """
   bit_string = str(bin(int(hex_string, base = 16))[2:]) # 0b will be sliced off
   bit_string_length = len(hex_string) * 4 # The real length of the bit string

   # We need the trailing zeros so make sure they are added here if missing
   num_lead_zeroes = bit_string_length - len(bit_string)

   return (("0" * num_lead_zeroes) + bit_string)
