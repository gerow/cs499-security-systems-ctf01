#!/usr/bin/python

import random
import binascii
import math

def rand_pop(elements):
    """
    Randomly pop an element from elements and return it
    """
    random.shuffle(elements)
    return elements.pop(0)

def long_to_byte_string(l, length):
  """
  This function is super hacky, and slow
  Might be useful to write this in a C module,
  but it's probably alright for now...'
  We expect l to be a long and length to be
  the length of the value represented by l
  in bits
  """
  hexform = "%x" % l
  if len(hexform) % 2 != 0:
    hexform = "0" + hexform
  bytes_form = binascii.unhexlify(hexform)
  while len(bytes_form) < math.ceil(length / 8.0):
    bytes_form = "\x00" + bytes_form
  return bytes_form

def byte_string_to_long(byte_string):
  """
  Reverses the long to byte string operation.
  It also returns a length for how many bits
  long the byte string is. Again, super hacky.
  """
  return long(binascii.hexlify(byte_string), 16), 8 * len(byte_string)
