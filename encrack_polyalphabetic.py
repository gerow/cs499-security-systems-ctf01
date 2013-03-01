#!/usr/bin/python

import copy
import sys
import collections

import encdec
import util

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

    self.__init_key()

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
    c_num = 0
    for i in range(m_i):
      c_num += len(self.messages[m_i])
    c_num += c_i
    slice_num = c_num % self.key_length
    self.set(self.messages[m_i][c_i], char, slice_num)

  def set(self, cipher, plain, alphabet):
    for k, v in self.key[alphabet].iteritems():
      if v == cipher:
        self.key[alphabet][k] = self.key[plain]
    self.key[alphabet][plain] = cipher

  def decrypt(self):
    self.e = encdec.Polyalphabetic()
    self.e.set_key(self.key)
    return [self.e.decrypt(m) for m in self.messages]

  def set_key_to_freq(self):
    split_messages = self.get_split_messages()
    for i in range(self.key_length):
      freport = self.a.frequency_report([split_messages[i]])
      print str(freport)
      for j, letter in enumerate(self.a.ordered_letters):
        print "i is " + str(i)
        print "j is " + str(j)
        self.key[i][letter] = freport[j][0]

  def score(self):
    chars_in_dict = self.a.fraction_chars_in_dict(self.decrypt())
    return chars_in_dict

  def partial_word_match_crack(self):
    self.load_new_messages()
    print "MESSAGES: " + str(self.messages)
    self.set_key_to_freq()
    print "MESSAGES " + str(self.decrypt())

  def crack(self):
    self.partial_word_match_crack()

  def get_split_messages(self):
    out = []
    for count in range(self.key_length):
      i = 0
      mstring = ""
      for m in self.messages:
        for c in m:
          if i % self.key_length == count:
            mstring += c
          i += 1
      out.append(mstring)

    return out

if __name__ == "__main__":
  directory = sys.argv[1]
  length = int(sys.argv[2])
  p = Polyalphabetic(directory, length)
  p.crack()
