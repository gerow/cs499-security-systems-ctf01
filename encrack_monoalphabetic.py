#!/usr/bin/python

import sys

import encdec

from encrack import *

class Monoalphabetic(EncryptionCracker):
  def __init__(self, directory):
    # Call parent's constructor
    super(Monoalphabetic, self).__init__(directory)
    self.a = Analysis()
    self.e = encdec.Monoalphabetic()

  def crack(self):
    frequency = self.a.frequency_report(self.messages)
    print frequency

if __name__ == "__main__":
  directory = sys.argv[0]
  m = Monoalphabetic(directory)
  m.crack()
