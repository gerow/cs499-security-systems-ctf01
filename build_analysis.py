#!/usr/bin/python

DIRECTORY = "etc/word_analysis"
TARGET = "etc/analysis_results"

import os
import util
import pickle

def build_analysis():
  letters = {}
  total_letters = 0
  filenames = os.listdir(DIRECTORY)
  for fn in filenames:
    with open(os.path.join(DIRECTORY, fn), "r") as f:
      for l in f:
        l = l.strip()
        l = util.strip_invalid_symbols(l)
        for c in l:
          try:
            letters[c] += 1
          except KeyError:
            letters[c] = 1
          total_letters += 1

  for k, v in letters.iteritems():
    letters[k] = v / float(total_letters)

  print letters

  with open(os.path.join(TARGET, "letter_frequency.analysis"), "w") as f:
    pickle.dump(letters, f)

if __name__ == "__main__":
  build_analysis()
