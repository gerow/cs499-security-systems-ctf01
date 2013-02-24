#!/usr/bin/python

import random
import binascii
import math

import encdec

"""
The symbols that are allowed for sending and receiving
"""
SYMBOLS = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
           "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
           "y", "z", ".", ",", "!", "?", " ")

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

def load_encdec(encdec_type, filename):
  """
  This function just loads an instance of the correct
  encdec given the argument and loads the keyfile given.

  The arguments are as follows:

  ma -- Monoalphabetic
  pa -- Polyalphabetic
  hp -- Homophonic
  pg -- Polygram
  st -- Stream
  no -- No (for testing)

  We ignore case for the type just to make things easier for the user.
  """

  encdec_type = encdec_type.lower()

  e = None

  if encdec_type == "ma":
    e = encdec.Monoalphabetic()
  elif encdec_type == "pa":
    e = encdec.Polyalphabetic()
  elif encdec_type == "hp":
    #e = encdec.Homophonic()
    raise NotImplementedError("That encryption type is not implemented yet")
  elif encdec_type == "pg":
    e = encdec.Polygram()
  elif encdec_type == "st":
    #e = encdec.Stream()
    raise NotImplementedError("That encryption type is not implemented yet")
  elif encdec_type == "no":
    e = encdec.No()
  else:
    raise ValueError("Invalid encryption type")

  e.load_key(filename)
  return e

def string_contains_valid_symbols(string):
  """
  Check to make sure each character is a valid symbol.
  We don't do caps coersion, so a capital letter
  will fail this.
  """
  for c in string:
    if c not in SYMBOLS:
      return False

  return True

def strip_invalid_symbols(string):
  """
  Strip invalid symbols from the string and return the
  stripped version.  We first do a conversion to lowercase
  so that capitalized characters aren't affected.
  """
  string  = string.lower()
  output = ""
  for c in string:
    if c in SYMBOLS:
      output += c

  return output
