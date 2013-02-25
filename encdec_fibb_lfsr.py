#!/usr/bin/python

import random

class FibbLFSR():
  """
  An implementation of a 16 bit lsfr
  """

  def __init__(self):
    self.__reg = 1
    self.INITIAL_BYTES_TO_POP_OFF = 300

  def set_key(self, key):
    """
    Set the initial state of the lsfr.  Note:
    it cannot be zero.  We also pop off a few extra bytes
    so that we don't reveal the key from the beginning.
    """
    if key == 0:
      raise ValueError("Initial lsfr value must be nonzero")
    self.__reg = key
    for i in range (self.INITIAL_BYTES_TO_POP_OFF):
      self.pop_byte()

  def generate_key(self):
    return random.randint(1, 65535)

  def pop_byte(self):
    out = 0
    for i in range(8):
      out |= self.pop_bit() << i
    return out

  def pop_bit(self):
    next_new_bit = self.__next_new_bit()
    val = (self.__reg) & 0x1
    self.__reg >>= 1
    self.__reg |= (next_new_bit << 0x10)
    return val

  def __next_new_bit(self):
    r = self.__reg
    tap_0 = r & 0x1
    tap_2 = (r >> 0x2) & 0x1
    tap_3 = (r >> 0x3) & 0x1
    tap_5 = (r >> 0x5) & 0x1
    return (((tap_0 ^ tap_2) ^ tap_3) ^ tap_5)
