#!/usr/bin/python

# Action IDs
ACTION_EMBED = 0
ACTION_EXTRACT = 1
ACTION_DETECT = 2
ACTION_VIS_ATK = 3
ACTION_FILTERED_VIS_ATK = 4

# Embedding IDs
LSB = 0
BPCS = 1

# Detection IDs
HIST_ATTACK = 0
VISUAL_ATTACK = 1
FVISUAL_ATTACK = 2

# File extensions
EXTENSIONS = [".jpg", ".jpeg", ".bmp", ".gif", "png"]

# File paths
PATH_COVER = "cover_objects/"
PATH_DETECT = "detect_statistics/"
PATH_EXTRACT = "extracted_objects/"
PATH_STEGO = "stego_objects/"

# File types
AUDIO = 0
IMAGE = 1
TEXT  = 2
VIDEO = 3
