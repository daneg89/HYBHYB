#!/usr/bin/python

from bit_manip import bits_to_bytes
from bit_manip import hex_to_bits
from os import path
import constants
import math
import subprocess

def calc_msg_header_len(num_embeddable_bits):
   """ Calculates the # of bits to use for a cover object's message length
   
   Params:
      num_embeddable_bits - Number of bits that we can actually use for embedding
   
   """
   return int(math.ceil(math.log(num_embeddable_bits, 2)))

def create_header(header_len, message_len):
   """ Creates the header that indicates how long a message is

   Params:
      header_len - Length that the header should be
      message_len - Length of the message that will be embedded

   Returns:
      String header with leading zeroes included

  """

   message_bits = bin(message_len)[2:]
   leading_zeroes = header_len - len(message_bits)

   if leading_zeroes > 0:
      header = (leading_zeroes * "0") + message_bits 
   else:
      header = message_bits

   return header

def get_file_extension(file_path):
   """ Determines the type of file specified by the file path

   Params:
      file_path - File path of the target file NOT including $PWD

   Returns:
      String of file extension. Ex: .jpg, .bmp, .png

   Throws:
      Exception when file is not found
   """
   pass

def get_file_type(file_path):
   """ Determines the type of file specified by the file path

   Params:
      file_path - File path of the target file NOT including $PWD

   Returns:
      Integer constant representing the file type (see constants.py)

   Throws:
      Exception when file is not found
   """

   if not file_exists(file_path):
      raise
   else:
      # TODO: implement this
      pass
   
   return constants.IMAGE

def file_to_bits(file_path):
   """ Performs a hexdump on a file and returns the bits
   Params:
      file_path - File path of the target file NOT including $PWD

   Returns:
      String of bits if successful

   Throws:
      Exception when file is not found
   """

   if not file_exists(file_path):
      raise Exception # TODO: Something
   else: 
      command = ["xxd", "-p", file_path]
      result = subprocess.Popen(command, stdout = subprocess.PIPE)
      bit_string = result.stdout.read().replace("\n", "")
      return hex_to_bits(bit_string)

def file_exists(file_path):
   """ Checks the file to see if it exists or not """
   return path.exists(file_path)
