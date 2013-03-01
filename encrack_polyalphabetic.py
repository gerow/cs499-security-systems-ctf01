#!/usr/bin/python

import copy
import sys

import encdec
import collections

from encrack import *

class Polyalphabetic(EncryptionCracker):
  def __init__(self, directory, length):
    super(Polyalphabetic, self).__init__(directory)
    self.a = Analysis()
    self.e = encdec.Polyalphabetic()
    self.d = Dictcheck()

    self.key = []
    self.key_length = length
    self.key_stack = []

  def __init_key(self):
    for i in range(self.key_length):
      self.key.append({})
    for s in util.SYMBOLS:
      for k in self.key:
        k[s] = s

  def push_key(self):
    self.key_stack.append(copy.copy(self.key))

  def pop_key(self):
    self.key = self.key_stack.pop()

  def clear_key_stack(self):
    self.key_stack = []

  def set_i_to_char(self, m_i, c_i, char):
    raise NotImplementedError("...")

  def decrypt(self):
    return [self.e.decrypt(m) for m in self.messages]

  def score(self):
    chars_in_dict = self.a.fraction_chars_in_dict(self.decrypt())
    return chars_in_dict

  def partial_word_match_crack(self):
    pass

  def crack(slef):
    self.partial_word_match_crack()

  def get_split_messaes(self):
    out = []
    for count in range(self.key_length):
      i = 0
      mstring = ""
      for m in self.messages:
        for c in m:
          if i % count == 0:
            mstring += c
          i += 1
      out.append(mstring)

    return out

if __name__ == "__main__":
  directory = sys.argv[1]
  length = int(sys.argv[2])
  p = Polyalphabetic(directory, length)
  p.crack()
