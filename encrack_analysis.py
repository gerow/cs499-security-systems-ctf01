#!/usr/bin/python

import encrack
import pickle
import os
import collections

import util

class Analysis:
  def __init__(self):
    self.d = encrack.Dictcheck()
    with open(os.path.join("etc", "analysis_results", "letter_frequency.analysis"), "r") as f:
      self.letter_frequency = pickle.load(f)

    self.__build_ordered_letters()
    self.most_common_words = []
    with open("etc/5000.txt", "r") as f:
      for l in f:
        self.most_common_words.insert(0, l)

  def __build_ordered_letters(self):
    s = sorted(self.letter_frequency.items(), key=lambda x: x[1])
    output = []
    s.reverse()
    for k, v in s:
      output.append(k)
    self.ordered_letters = tuple(output)

  def frequency_report(self, messages):
    """
    Assume messages is a list of strings
    Return a dict listing each character
    in the messages and the fraction of
    the total message that it is a part of
    """
    out = {}
    for l in util.SYMBOLS:
      out[l] = 0
    for message in messages:
      for c in message:
        try:
          out[c] += 1
        except KeyError:
          out[c] = 1
    total_len = 0
    for message in messages:
      total_len += len(message)
    if total_len == 0:
      return out
    for k,v in out.iteritems():
      out[k] = float(v)/float(total_len)
    sorted_out = sorted(out.items(), key=lambda x: x[1])
    sorted_out.reverse()
    return sorted_out

  def __remove_punctuation_cleverly(self, word):
    if word[-1] in [",", ".", "?", "!"]:
      return word[:-1]
    return word

  def is_most_common_word(self, word):
    word = self.__remove_punctuation_cleverly(word)
    return word in self.most_common_words

  def common_word_score(self, word):
    if not self.is_most_common_word(word):
      return 0.0
    return 1.0 - self.most_common_words.index(word)/5000.0

  def common_words_score(self, messages):
    score = 0.0
    for m in messages:
      for word in m.split():
        score += self.common_word_score(word)

    return score

  def detect_odd_space(self, messages):
    """
    Return a list of indicies for each
    message if we detect odd spaces.  That
    includes spaces at the beginning or end
    of the message or multiple spaces next to
    each other. In the case of multiple spaces
    next to each other we list the index of the
    first instance unless we have three spaces
    in which case we list the first two and so on
    """
    problems = []
    for i, message in enumerate(messages):
      # Create a new entry for this message
      problems.append([])
      # Ignore message if empty
      if not message:
        continue
      if message[0] == " ":
        problems[i].append(0)
      for j, c in enumerate(message):
        try:
          if c == " " and message[j + 1] == " ":
            problems[i].append(j)
        except IndexError:
          # Just ignore it, we're cool
          pass
      if message[-1] == " ":
        problems[i].append(len(message) - 1)
    # Return an empty list if it is nothing but
    # empty list (so this can be used with an if
    # statement)

    for message_problem in problems:
      if message_problem:
        return problems
    return []

  #def detect_odd_punctuation(self, messages):
  #  for m in messages:
  #    for i, c in enumerate(messages):
  #      try:
  #        if c == "." && (messages[i + 1] != " " || i == 0):
  #          return True
  #        if c == "," && (messages[i + 1] != " " || i == 0 || i == len(messages) - 1):
  #          return True
  #        if c == 
  #      except IndexError:
  #        pass


  def fraction_chars_in_dict(self, messages):
    """
    Works much like the one in dictcheck except it
    operates on an array of messages
    """
    output = 0.0
    count, counts = self.__count_letters(messages)
    total_len = count

    if count == 0:
      return 0.0

    for i, m in enumerate(messages):
      weight = float(counts[i])/total_len
      output += self.d.fraction_chars_in_dict(m) * weight

    return output
  
  def __count_letters(self, messages):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i","j",
               "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
               "u", "v", "w", "x", "y", "z"]
    count = 0
    counts = collections.deque()
    for m in messages:
      strcount = 0
      for c in m:
        if c in letters:
          count += 1
          strcount += 1
      counts.append(strcount)
    return count, counts
