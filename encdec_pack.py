#!/usr/bin/python

import util

class Packer:
  """
  This class is designed to allow us to pack all the allowed
  values in this excersize into their minimal 5 bit values.
  While this does make things slightly harder to solve, it also
  makes it to where some of our ciphers are more effective at lower
  key sizes (specifically substitution ciphers)
  @author gerow
  """
  def __init__(self):
    self.__generate_packing_dict()
    self.__generate_inv_packing_dict()

  def __generate_packing_dict(self):
    # could have actually generated this, but whatever
    self.__packing_dict = {
        "a":0x00,
        "b":0x01,
        "c":0x02,
        "d":0x03,
        "e":0x04,
        "f":0x05,
        "g":0x06,
        "h":0x07,
        "i":0x08,
        "j":0x09,
        "k":0x0a,
        "l":0x0b,
        "m":0x0c,
        "n":0x0d,
        "o":0x0e,
        "p":0x0f,
        "q":0x10,
        "r":0x11,
        "s":0x12,
        "t":0x13,
        "u":0x14,
        "v":0x15,
        "w":0x16,
        "x":0x17,
        "y":0x18,
        "z":0x19,
        ".":0x1a,
        ",":0x1b,
        "!":0x1c,
        "?":0x1d,
        " ":0x1e,
        "EOF": 0x1f
    }

  def __generate_inv_packing_dict(self):
    self.__inv_packing_dict = {}
    for k, v in self.__packing_dict.iteritems():
      self.__inv_packing_dict[v] = k

  def pack(self, text):
    """
    This function packs the text given into a smaller binary
    representation since the range of characters availible to us
    is relatively small.  This should give good results with certain
    block ciphers even if the block size is relatively small.
    It returns the value as a long
    """
    # Since we only have 31 symbols (32 with EOF) we only need 5 bits to represent each one
    b = 0 
    for i, c in enumerate(text):
      shift = 5 * i
      b |= (self.__packing_dict[c] << shift)

    shift += 5
    b |= (self.__packing_dict["EOF"] << shift)
    return util.long_to_byte_string(b, shift * 5)

  def unpack(self, byte_string):
    shift = 0
    string = ""

    number, length = util.byte_string_to_long(byte_string)
    while shift < length:
      val = (number >> shift) & 0x1f
      c = self.__inv_packing_dict[val]
      if c == "EOF":
        return string
      string += c
      shift += 5

    return string
