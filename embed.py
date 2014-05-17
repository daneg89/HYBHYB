#!/usr/bin/python

from lsb import lsb_embed
from bpcs import bpcs_embed

#
# Generic embedding function that determines how to embed a file
#
# Params:
#   data - [Default]Dict that carries the following information
#        > 
#
def embed(data):
  lsb_embed(None, None)
  bpcs_embed(None, None)


embed(None)
