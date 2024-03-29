#!/usr/bin/python

import util

class Dictcheck(object):
  """
  This class provides a handful of useful
  utilities for checking strings against
  dictionary values
  """

  def __init__(self):
    DICTFILE = "words.txt"
    self.words_set = set()
    self.words_list = list()
    self.load_dict(DICTFILE)

  def load_dict(self, filename):
    with open(filename, "r") as f:
      for word  in f.readlines():
        word = word.strip()
        word = util.strip_punctuation(word)
        self.words_list.append(word)
      self.words_set = set(self.words_list)

  def word_in_dict(self, word):
    """
    Check to see if the given word is in the dict.
    If it is, return true, otherwise return false.  Note that word with upper case characters or
    punctuation will always fail.
    """
    return word in self.words_set

  def fraction_chars_in_dict(self, string):
    """
    This function expects a string containing
    space seperated words.  It will look up
    each word in the set and see if is in the dict.

    It will then generate a value that is #chars that
    are words divided by #chars in the string. Do not
    count towards either.  In addition, any punctuation
    is stripped
    """
    # Check if len is 0 (so we don't overflow on accident)
    # string = util.strip_punctuation(string)
    if string[-1] in [".", ",", "!", "?"]:
      string = string[:-1]
    if len(string) == 0:
      return 0.0
    words = string.split()
    good_chars = 0
    total_chars = 0
    for word in words:
      total_chars += len(word)
      if self.word_in_dict(word):
        good_chars += len(word)

    return float(good_chars) / float(total_chars)

  def get_partial_word_matches(self, string):
    out = []
    for word in self.words_set:
      word = util.strip_invalid_symbols(word)
      if len(word) == len(string):
        match_count = 0
        for i in range(len(word)):
          if word[i] == string[i]:
            match_count += 1

        out.append({ "word":word, "count":match_count})

    out.sort(key=lambda entry: entry["count"])
    out.reverse()
    return out
