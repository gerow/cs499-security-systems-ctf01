#!/usr/bin/python

import copy
import sys
import collections
import random
import math

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
    self.AVG_WORD_LENGTH = 5.2

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

  def partial_word_match_crack(self):
    print "SPLIT MESSAGES: " + str(self.get_split_messages())
    self.load_new_messages()
    print "MESSAGES: " + str(self.messages)
    self.set_key_to_freq()
    print "initial decryption: " + str(self.decrypt())
    print "generating likely candidates for space character..."
    space_freqs = self.gen_space_freqs(16)
    print "ranking candidate space characters..."
    space_freqs = self.order_space_freqs(space_freqs)
    for sp in space_freqs:
      self.set_spaces(sp)
      if self.crack_with_space_setting():
        print "DONE!"
        return

  def order_space_freqs(self, sp):
    results = collections.deque()
    for i, s in enumerate(sp):
      if i % 20000 == 0:
        print "calculating deviation for iteration " + str(i) + " of " + str(len(sp)) + " (" + str(float(i)/len(sp) * 100) + "%)"
      self.set_spaces(s)
      results.append([s, math.fabs(self.AVG_WORD_LENGTH -  self.avg_word_length())])
    results = list(results)
    print "sorting list (this could take a while)"
    results.sort(key=lambda entry: entry[1])
    return [entry[0] for entry in results]


  def avg_word_length(self):
    decrypted = self.decrypt()
    lengths = collections.deque()
    for m in decrypted:
      for w in m.split():
        w = self.remove_normal_punc(w)
        lengths.append(len(w))
    return float(sum(lengths))/len(lengths)

  def set_spaces(self, sp):
    for i, v in enumerate(sp):
      self.set(v, " ", i)

  def set(self, cipher, plain, alphabet):
    for k, v in self.key[alphabet].iteritems():
      if v == cipher:
        self.key[alphabet][k] = self.key[alphabet][plain]
    self.key[alphabet][plain] = cipher

  def crack_with_space_setting(self):
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
    out = collections.deque()
    for m in split_messages:
      freq_reports.append(self.a.frequency_report([m]))

    for i in range(num_per**len(freq_reports)):
      if i % 20000 == 0:
        print "generating iteration " + str(i) + " of " + str(num_per**len(freq_reports)) + " (" + str(float(i)/num_per**len(freq_reports) * 100) + "%)"
      new_one = collections.deque()
      for j, f in enumerate(freq_reports):
        new_one.append(freq_reports[j][i / num_per**j % num_per][0])
      out.append(new_one)

    return out

  def crack(self):
    if self.method == "sa":
      self.simulated_annealing_crack()
    elif self.method == "pm":
      self.partial_word_match_crack()
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
