#!/usr/bin/python

import sys

import encdec
import util
import copy
import random

from encrack import *

class Monoalphabetic(EncryptionCracker):
  def __init__(self, directory):
    # Call parent's constructor
    super(Monoalphabetic, self).__init__(directory)
    self.a = Analysis()
    self.e = encdec.Monoalphabetic()
    self.d = Dictcheck()
    self.key = {}
    self.frozen_symbol = {}
    self.__init_key()
    self.key_stack = []

  def __init_key(self):
    for s in util.SYMBOLS:
      self.key[s] = s
    for s in self.frozen_symbol:
      self.frozen_symbol = False

  def push_key(self):
    self.key_stack.append(copy.copy(self.key))

  def pop_key(self):
    self.key = self.key_stack.pop()

  def clear_key_stack(self):
    self.key_stack = []

  def set(self, cipher, plain):
    for k, v in self.key.iteritems():
      if v == cipher:
        self.key[k] = self.key[plain]
    self.key[plain] = cipher

  def random_set_key(self):
    plain_set = copy.copy(list(util.SYMBOLS))
    plain_set.remove(" ")
    cipher_set = copy.copy(list(util.SYMBOLS))
    cipher_set.remove(self.key[" "])

    plain_pick = random.choice(plain_set)
    cipher_pick = random.choice(cipher_set)
    self.set(cipher_pick, plain_pick)

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

  def temp(self, p):
    """
    Linear temperature decreasing
    """
    #return -p**2 + 1
    return 1 - p

  def score(self):
    chars_in_dict = self.a.fraction_chars_in_dict(self.decrypt())
    #common_word_score = self.a.common_words_score(self.decrypt())
    return chars_in_dict

  def acceptance_probability(self, score, new_score, temp):
    if new_score >= score:
      return 1.0
    return temp

  def remove_normal_punc(self, word):
    if word[-1] in (".", ",", "!", "?"):
      return word[:-1]
    return word

  def partial_word_match_crack(self):
    """
    Try to crack using a partial word match approach
    It's kinda a mess... but it was written at 3am during
    a flash of inspiration
    """
    self.load_new_messages()
    print "MESSAGES: " + str(self.messages)
    # Set the values by frequency first just as a
    # good starting point
    self.set_key_to_freq()

    # Cycle over the list 1000 times
    decrypted = self.decrypt()
    for i in range(1):
      for m_i in range(len(decrypted)):
        split_words = decrypted[m_i].split()
        for w_i in range(len(split_words)):
          word = self.remove_normal_punc(split_words[w_i])
          if self.d.word_in_dict(word):
            continue
          partials = self.d.get_partial_word_matches(word)
          #print "With word " + word
          #print "Suggested partials " + str(partials)
          best_score = self.score()
          best_key = self.key
          common_word_score = 0.0
          for p in partials:
            self.push_key()
            if p["count"] == 0:
              break
            for k, c in enumerate(p["word"]):
              cipher_letter = self.messages[m_i][self.get_char_index(m_i, w_i, k)]
              #print "ciphertext " + cipher_letter
              #print "suggested character " + c
              c = c.lower()
              self.set(cipher_letter, c)
            score = self.score()
            if score > best_score:
              print "New best scoring is " + str(self.decrypt())
              print "It has a score of " + str(self.score())
              if self.score() == 1.0:
                return
              best_score = score
              best_key = self.key
            elif score == best_score:
              new_common_word_score = self.a.common_word_score(p["word"])
              if new_common_word_score > common_word_score:
                common_word_score = new_common_word_score
                best_key = self.key
            self.pop_key()
          self.key = best_key
          decrypted = self.decrypt()
          split_words = decrypted[m_i].split()

    print str(self.decrypt())


  def get_char_index(self, m_i, w_i, c_i):
    ccount = 0
    decrypted = self.decrypt()
    for i, word in enumerate(decrypted[m_i].split()):
      if i == w_i:
        return ccount + c_i
      else:
        ccount += len(word) + 1


  def simulated_annealing_crack(self):
    """
    Try to crack using a simulated annealing based
    appraoch
    """
    self.load_new_messages()
    print "MESSAGES: " + str(self.messages)
    self.set_key_to_freq()
    print self.decrypt()
    # First, we try to guess where the spaces are
    f_report = self.a.frequency_report(self.messages)
    print f_report
    self.set(f_report[0][0], " ")
    print self.key
    print self.decrypt()

    # We assume that the most common character is space...
    # Might want to try something else too...
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
    print "Using key " + str(self.key)

  def crack(self):
    self.partial_word_match_crack()
    #self.simulated_annealing_crack()

if __name__ == "__main__":
  directory = sys.argv[1]
  m = Monoalphabetic(directory)
  m.crack()
