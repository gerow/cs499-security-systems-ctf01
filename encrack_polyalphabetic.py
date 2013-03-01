#!/usr/bin/python

import copy

import encdec

from encrack import *

class Polyalphabetic(EncryptionCracker):
  def __init__(self, directory, length):
    super(Polyalphabetic, self).__init__(directory)
    self.a = Analysis()
    self.e = encdec.Polyalphabetic()
    self.d = Dictcheck()

    self.key = []
    self.key_length
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
    self.e.set_key(self.key)
    out = []
