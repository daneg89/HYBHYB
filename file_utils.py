#!/usr/bin/python

from bit_manip import hex_to_bits
from os import path
import subprocess

def convert_file_to_bits(file_path):
   """ Performs a hexdump on a file and returns the bits

   Params:
      file_path - File path of the target file NOT including $PWD
   Returns:
      String/None - String of bits if successful, None if problems with file
   """
   if not file_exists(file_path):
      return None
   else: 
      command = ["xxd", "-p", file_path]
      result = subprocess.Popen(command, stdout = subprocess.PIPE)
      bit_string = result.stdout.read().rstrip()
      return hex_to_bits(bit_string)

def file_exists(file_path):
   """ Checks the file to see if it exists or not """
   return path.exists(file_path)
