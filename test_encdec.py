#!/usr/bin/python

import unittest
import encdec

class BasicEncryptionTestCase(unittest.TestCase):
  """
  This test case should be able to test all the
  encryptordecryptors using some basic tests. In
  order to be compatible the EncryptorDecryptor must
  use some default values to generate a key if
  no arguments are provided
  @author gerow
  """
  def setUp(self):
    self.enc_decs = []
    self.enc_decs.append(encdec.Monoalphabetic())

  def assert_encrypt_text(self, text):
    """
    Small function to help us out.  Just tries encrypting and
    decrypting the given text and seeing if it stays the same
    """
    plaintext = text
    for enc_dec in self.enc_decs:
      enc_dec.set_key(enc_dec.generate_key(None))
      ciphertext = enc_dec.encrypt(plaintext)
      self.assertEqual(enc_dec.decrypt(ciphertext), plaintext,
          'incorrect decryption using ' + str(enc_dec))


  def test_hello(self):
    """
    Most basic test.  Just encrypts hello and sees
    if it is able to decrypt back.
    """
    self.assert_encrypt_text("hello")

  def test_complete(self):
    """
    Test all the availible symbol set
    """
    self.assert_encrypt_text("abcdefghijklmnopqrstuvwxyz.,!? ")

  def test_double_complete(self):
    """
    Test all the availible symbol set twice.  This might help test
    polyalphabetic of stream siphers
    """
    self.assert_encrypt_text("abcdefghijklmnopqrstuvwxyz.,!? " * 2)

  def test_triple_complete(self):
    """
    Same reasoning as test_double_complete
    """
    self.assert_encrypt_text("abcdefghijklmnopqrstuvwxyz.,!? " * 3)

  def tearDown(self):
    self.enc_decs = None

class MonoalphabeticTestCase(unittest.TestCase):
  """
  Test case to specifically test the Monoalphabetic implementation
  @author gerow
  """
  def setUp(self):
    self.ma_instance = encdec.Monoalphabetic()

  def tearDown(self):
    self.ma_instance = None

if __name__ == "__main__":
  unittest.main()
