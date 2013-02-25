#!/usr/bin/python

import unittest
import encrack

class DictcheckTestCase(unittest.TestCase):
  """
  Test the Dictcheck class
  """

  def setUp(self):
    self.d = encrack.Dictcheck()

  def test_word_in_dict(self):
    words = (("hello", True),
             ("goodbye", True),
             ("lkjealkj", False),
             ("emergency", True),
             ("encryption", True))
    for word in words:
      truth_value = self.d.word_in_dict(word[0])
      self.assertEqual(truth_value,word[1],
          "truth values for word_in_dict do not match! (got " + str(truth_value) + " expected " + str(word[1]))

  def test_fraction_chars_in_dict(self):
    strings = (("hello there this is words!", 1.0),
               ("oh, lkje whatever", 10.0/14.0))

    for string in strings:
      frac = self.d.fraction_chars_in_dict(string[0])
      self.assertEqual(frac, string[1],
          "fractions do not match for " + string[0] + ". got " + str(frac) + " expected " + str(string[1]))

  def tearDown(self):
    self.d = None

if __name__ == "__main__":
  unittest.main()
