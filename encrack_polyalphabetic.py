#!/usr/bin/python

import copy
import sys
import collections
import random

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
        self.key[alphabet][k] = self.key[alphabet][plain]
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

  def temp(self, p):
    """
    Linear temperature decreasing
    """
    #return -p**2 + 1
    return 1 - p

  def acceptance_probability(self, score, new_score, temp):
    if new_score >= score:
      return 1.0
    return temp

  def random_set_key(self):
    plain_set = copy.copy(list(util.SYMBOLS))

    plain_pick = random.choice(util.SYMBOLS)
    cipher_pick = random.choice(util.SYMBOLS)
    alphabet = random.randint(0, self.key_length - 1)
    self.set(cipher_pick, plain_pick, alphabet)

  def simulated_annealing_crack(self):
    self.load_new_messages()
    print "MESSAGES: " + str(self.messages)
    self.set_key_to_freq()
    print "initial decryption: " + str(self.decrypt())

    kmax = 10000000
    k = 0
    best_key = copy.copy(self.key)
    best_score = self.score()
    s = best_score

    while k < kmax:
      t = self.temp(float(k)/kmax)
      self.push_key()
      self.random_set_key()
      snew = self.score()
      if self.acceptance_probability(s, snew, t) > random.random():
        s = snew
        self.clear_key_stack()
      else:
        self.pop_key()
      if s > best_score:
        best_score = s
        best_key = copy.copy(self.key)
        print "New best key gives us " + str(self.decrypt())
        print "It has a score of " + str(self.score())
      if k % 10000 == 0:
        print "On iteration " + str(k)
        self.load_new_messages()
      k += 1

    self.key = best_key
    print "Best scoring decryption is " + str(self.decrypt())
    print "Using key" + str(self.key)

  def crack(self):
    self.simulated_annealing_crack()
    #self.partial_word_match_crack()

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
