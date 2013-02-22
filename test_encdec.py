#!/usr/bin/python

import unittest
import encdec

class BasicEncryptionTestCase(unittest.TestCase):
  def setUp(self):
    self.enc_decs = []
    self.enc_decs.append(encdec.Monoalphabetic())

  def assert_encrypt_text(self, text):
    plaintext = text
    for enc_dec in self.enc_decs:
      enc_dec.set_key(enc_dec.generate_key(None))
      ciphertext = enc_dec.encrypt(plaintext)
      self.assertEqual(enc_dec.decrypt(ciphertext), plaintext,
          'incorrect decryption using ' + str(enc_dec))


  def test_hello(self):
    self.assert_encrypt_text("hello")

  def test_complete(self):
    self.assert_encrypt_text("abcdefghijklmnopqrstuvwxyz.,!? ")

  def test_double_complete(self):
    self.assert_encrypt_text("abcdefghijklmnopqrstuvwxyz.,!? " * 2)

  def test_triple_complete(self):
    self.assert_encrypt_text("abcdefghijklmnopqrstuvwxyz.,!? " * 3)

  def tearDown(self):
    self.enc_decs = None

class MonoalphabeticTestCase(unittest.TestCase):
  def setUp(self):
    self.ma_instance = encdec.Monoalphabetic()

  def tearDown(self):
    self.ma_instance = None

if __name__ == "__main__":
  unittest.main()
