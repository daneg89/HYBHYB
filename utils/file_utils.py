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

def get_file_extension(file_name):
   """ Determines the type of file specified by the file name

   Params:
      file_name - File name with the extension

   Returns:
      String of file extension. Ex: .jpg, .bmp, .png

   Throws:
      Exception when bad extension is given
   """

   # Get last 5 chars in case of jpeg
   extension = file_name[-5:]
   if extension[0] == ".": # .jpeg
      if extension[1:] in constants.EXTENSIONS: 
         pass
      else: # Invalid extension
         raise Exception # TODO: custom exception?
   else: # .bmp, .png, .gif, .jpg
      extension = file_name[-4:]
      if extension[1:] in constants.EXTENSIONS:
         pass
      else: # Invalid extension
         raise Exception # TODO: custom exception?

   return extension

def get_file_name_from_path(file_path):
   """ Parses and returns a file name

   Params:
      file_path - String that has a path and a file name
      
   Returns:
      Name of the file with extension

   """
   # Keep removing the path until its gone
   while file_path.find("/") != -1:
      file_path = file_path[file_path.find("/") + 1:]

   return file_path

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
