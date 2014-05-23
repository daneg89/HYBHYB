#!/usr/bin/python

from bit_manip import bits_to_bytes
from bit_manip import hex_to_bits
from os import path
import constants
import subprocess

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
      raise # TODO: Something
   else: 
      command = ["xxd", "-p", file_path]
      result = subprocess.Popen(command, stdout = subprocess.PIPE)
      bit_string = result.stdout.read().replace("\n", "")
      return hex_to_bits(bit_string)

def file_exists(file_path):
   """ Checks the file to see if it exists or not """
   return path.exists(file_path)
