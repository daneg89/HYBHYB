#!/usr/bin/python

from PIL import Image
import math

def histogram_attack(img_path):
   """ Performs a histogram attack on a specified image to see if it is LSB
       embedded

   Params:
      img_path - Path to the image that we want to analyze

   """
   acceptance_level = 75 # 30% of values
   diff_cap = 50
   target_img = Image.open(img_path)
   img_histogram = target_img.histogram()

   # Get rid of the zero vals, if any
   img_histogram = filter(lambda val: val > 0, img_histogram)
   num_pixels = sum(img_histogram)

   # Get the differences between each pair of values
   pair_differences = [abs(img_histogram[i] - img_histogram[i + 1]) 
                       for i in range(0, len(img_histogram), 2)]

   small_pairs = 0 # Number of pairs that are lower than the difference cap
   for i in range(0, len(pair_differences)):
      if pair_differences[i] <= diff_cap:
         small_pairs += 1

   # Final result
   if small_pairs >= acceptance_level:
      chance_embedded = float(small_pairs) / len(pair_differences)
      print "Image at", img_path, "is", chance_embedded, "% likely to contain a hidden message!"
   else:
      chance_embedded = 1.0 - (float(small_pairs) / len(pair_differences))
      print "Image at", img_path, "is", chance_embedded, "% unlikely to contain a hidden message!"
