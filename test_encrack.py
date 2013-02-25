#!/usr/bin/python

import unittest
import encrack
import os
import shutil
import time

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
      self.assertEqual(truth_value, word[1])

  def test_fraction_chars_in_dict(self):
    strings = (("hello there this is words!", 1.0),
               ("oh, lkje whatever", 10.0/14.0))

    for string in strings:
      frac = self.d.fraction_chars_in_dict(string[0])
      self.assertEqual(frac, string[1])

  def tearDown(self):
    self.d = None

class EncryptionCrackerTestCase(unittest.TestCase):
  def setUp(self):
    self.e = encrack.EncryptionCracker("temp_test")
    os.mkdir("temp_test")

  def test_encryption_cracker_load_messages(self):
    # Make two files in temp_test in some order
    first_message = "this is the first message"
    second_message = "this is the second message"
    with open(os.path.join("temp_test", "test0"), "w") as f:
      f.write(first_message)
    time.sleep(0.1)
    with open(os.path.join("temp_test", "test1"), "w") as f:
      f.write(second_message)
    self.e.load_new_messages()

    self.assertEqual(2, len(self.e.messages))
    self.assertEqual(first_message, self.e.messages[0])
    self.assertEqual(second_message, self.e.messages[1])

  def test_encryption_cracker_load_new_messages(self):
    # First make one file
    first_message = "first message"
    second_message = "second message"
    third_message = "yeah, a third message!"

    with open(os.path.join("temp_test", "test0"), "w") as f:
      f.write(first_message)
    # Sleep to make sure the mtimes are far enough
    # apart
    time.sleep(0.1)

    # Now get it to load this one
    self.e.load_new_messages()

    self.assertEqual(1, len(self.e.messages))
    self.assertEqual(first_message, self.e.messages[0])

    # Now add two more
    with open(os.path.join("temp_test", "test1"), "w") as f:
      f.write(second_message)
    # Sleep to make sure the mtimes are far enough apart
    time.sleep(0.1)
    with open(os.path.join("temp_test", "test2"), "w") as f:
      f.write(third_message)

    self.e.load_new_messages()

    self.assertEqual(3, len(self.e.messages))
    self.assertEqual(second_message, self.e.messages[1])
    self.assertEqual(third_message, self.e.messages[2])

  def tearDown(self):
    self.e = None
    shutil.rmtree("temp_test")

class AnalysisTestCase(unittest.TestCase):
  def setUp(self):
    self.a = encrack.Analysis()

  def test_frequency_report(self):
    message0 = "hello there"
    message1 = "alright, neato"

    t = len(message0) + len(message1)

    e = { "h":3.0/t,
          "e":4.0/t,
          "l":3.0/t,
          "o":2.0/t,
          " ":2.0/t,
          "t":3.0/t,
          "r":2.0/t,
          "a":2.0/t,
          "i":1.0/t,
          "g":1.0/t,
          ",":1.0/t,
          "n":1.0/t
        }
    report = self.a.frequency_report([message0, message1])

    self.assertEqual(e, report)

  def tearDown(self):
    self.a = None

class AnalysisTestCase(unittest.TestCase):
  def setUp(self):
    self.a = encrack.Analysis()

  def test_detect_odd_space_none(self):
    no_odd_space = ["there is no odd space in this message",
                    "nor is there in this one!"]
    self.assertEqual([], self.a.detect_odd_space(no_odd_space))

  def test_detect_odd_space_middle(self):
    middle_odd_space = ["no odd space here",
                        "but there  is in here"]
    expected_array = [[], [9]]

    self.assertEqual(expected_array, self.a.detect_odd_space(middle_odd_space))

  def test_detect_odd_space_beginning_and_end(self):
    odd_space = [" odd space at beginning",
                 "odd space at end "]

    expected_array = [[0], [16]]
    self.assertEqual(expected_array, self.a.detect_odd_space(odd_space))

  def tearDown(self):
    self.a = None

if __name__ == "__main__":
  unittest.main()
