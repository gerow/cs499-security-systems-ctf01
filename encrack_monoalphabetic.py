#!/usr/bin/python

import sys

import encdec
import util

from encrack import *

class Monoalphabetic(EncryptionCracker):
  def __init__(self, directory):
    # Call parent's constructor
    super(Monoalphabetic, self).__init__(directory)
    self.a = Analysis()
    self.e = encdec.Monoalphabetic()
    self.key = {}
    self.frozen_symbol = {}
    self.__init_key()

  def __init_key(self):
    for s in util.SYMBOLS:
      self.key[s] = s
    for s in self.frozen_symbol:
      self.frozen_symbol = False

  def set(self, cipher, plain):
    for k, v in self.key.iteritems():
      if v == cipher:
        self.key[k] = self.key[plain]
    self.key[plain] = cipher

  def decrypt(self):
    self.e = encdec.Monoalphabetic()
    self.e.set_key(self.key)
    out = []
    for m in self.messages:
      out.append(self.e.decrypt(m))
    return out

  def set_key_to_freq(self):
    f_report = self.a.frequency_report(self.messages)
    for i, letter in enumerate(self.a.ordered_letters):
      self.key[letter] = f_report[i][0]

  def crack(self):
    self.load_new_messages()
    print "MESSAGES: " + str(self.messages)
    self.set_key_to_freq()
    print self.decrypt()
    # First, we try to guess where the spaces are
    f_report = self.a.frequency_report(self.messages)
    print f_report
    for i in range(3):
      self.set(f_report[i][0], " ")
      print self.key
      print self.decrypt()

if __name__ == "__main__":
  directory = sys.argv[1]
  m = Monoalphabetic(directory)
  m.crack()
