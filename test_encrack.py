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

if __name__ == "__main__":
  unittest.main()
