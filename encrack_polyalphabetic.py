#!/usr/bin/python

import copy
import sys
import collections
import random

import encdec
import util

from encrack import *

class Polyalphabetic(EncryptionCracker):
  def __init__(self, directory, length, method):
    super(Polyalphabetic, self).__init__(directory)
    self.a = Analysis()
    self.e = encdec.Polyalphabetic()
    self.d = Dictcheck()

    self.key = []
    self.key_length = length
    self.key_stack = []

    self.method = method

    self.wordi_cache = {}

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

  def get_alphabet_number(self, m_i, w_i, c_i):
    ccount = 0
    decrypted = self.decrypt()
    for i, m in decrypted:
      if i != mi_wi:
        ccount += len(m)
      else:
        break
    for i, word in enumerate(decrypted[m_i].split()):
      if i == w_i:
        return (ccount + c_i) % self.key_length
      else:
        ccount += len(word) + 1

  def random_set_key(self):
    plain_set = copy.copy(list(util.SYMBOLS))

    plain_pick = random.choice(util.SYMBOLS)
    cipher_pick = random.choice(util.SYMBOLS)
    alphabet = random.randint(0, self.key_length - 1)
    self.set(cipher_pick, plain_pick, alphabet)

  def partial_word_match_crack(self):

    decrypted = self.decrypt()
    for i in range(14):
      print "NOW ON ITERATION " + str(i)
      for m_i in range(len(decrypted)):
        split_words = decrypted[m_i].split()
        c_i = 0
        for w_i in range(len(split_words)):
          print "Split words is " + str(split_words)
          print "w_i is " + str(w_i)
          try:
            word = self.remove_normal_punc(split_words[w_i])
          except IndexError:
            break
          if self.d.word_in_dict(word):
            continue
          partials = self.d.get_partial_word_matches(word)
          best_score = self.score()
          best_key = self.key
          common_word_score = 0.0
          for p in partials:
            self.push_key()
            if p["count"] == 0:
              break
            for k, c in enumerate(p["word"]):
              cipher_letter = self.messages[m_i][self.get_char_index(m_i, w_i, k)]
              plain_letter = c
              alphabet_number = self.get_alphabet_number(m_i, w_i, k)
              self.set(cipher_letter, plain_letter, alphabet_number)
              self.set_i_to_char(m_i, c_i + k, c)
            score = self.score()
            if score > best_score:
              print "New best scoring is " + str(self.decrypt())
              print "It has a score of " + str(self.score())
              c = c.lower()
              if self.score() == 1.0:
                print "Good score!"
                return True
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
        try:
          c_i += len(split_words[w_i]) + 1
        except IndexError:
          break
      if self.score() < 0.20:
        print "Unlikely space candidate"
        return

  def get_char_index(self, m_i, w_i, c_i):
    if (m_i, w_i) in self.wordi_cache:
      return self.wordi_cache[(m_i, w_i)] + c_i
    ccount = 0
    decrypted = self.decrypt()
    for i, word in enumerate(decrypted[m_i].split()):
      if i == w_i:
        self.wordi_cache[(m_i, w_i)] = ccount
        return ccount + c_i
      else:
        ccount += len(word) + 1

  def remove_normal_punc(self, word):
    if word[-1] in (".", ",", "!", "?"):
      return word[:-1]
    return word

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

    while k < kmax or s < 0.9:
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

  def gen_space_freqs(self, num_per):
    freq_reports = []
    split_messages = self.get_split_messages()
    curr_number = []
    out = []
    for m in split_messages:
      freq_reports.append(self.a.frequency_report([m]))
      out.append([])
    for i in range(len(split_messages)):
      curr_number.append(0)

    out_i = 0
    while curr_number:
      out.append([])
      for i, n in enumerate(curr_number):
        out[out_i].append(freq_reports[i][n][0])
      out_i += 1 
      curr_number = self.__inc_curr_number(curr_number, num_per)
      print "curr number: " + str(curr_number)
    return out

  def __inc_curr_number(self, curr_number, num_per):
    print "curr number: " + str(curr_number)
    for i, v in enumerate(curr_number):
      curr_number[i] += 1
      if curr_number[i] == num_per - 1:
        curr_number[i] = 0
        if i == len(curr_number) - 1:
          return False 
        continue
      return curr_number

  def crack(self):
    if self.method == "sa":
      self.simulated_annealing_crack()
    elif self.method == "pm":
      self.load_new_messages()
      print "MESSAGES: " + str(self.messages)
      self.set_key_to_freq()
      print "initial decryption: " + str(self.decrypt())

      space_freqs = self.gen_space_freqs(2)

      print "space freqs " + str(space_freqs)

      while self.partial_word_match_crack():
        pass
    else:
      print "Invalid method type"

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
  method = sys.argv[3]
  p = Polyalphabetic(directory, length, method)
  p.crack()
