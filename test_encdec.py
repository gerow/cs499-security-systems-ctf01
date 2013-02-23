#!/usr/bin/python

import unittest
import encdec
import util
import copy

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
    self.enc_decs.append(encdec.Polygram())

    self.other_enc_decs = []
    for enc_dec in self.enc_decs:
      self.other_enc_decs.append(copy.deepcopy(enc_dec))

  def assert_encrypt_text(self, text):
    """
    Small function to help us out.  Just tries encrypting and
    decrypting the given text and seeing if it stays the same
    """
    plaintext = text
    for enc_dec in self.enc_decs:
      enc_dec.set_key(enc_dec.generate_key(None))
      ciphertext = enc_dec.encrypt(plaintext)
      decryptedtext = enc_dec.decrypt(ciphertext)
      self.assertEqual(decryptedtext, plaintext,
          'incorrect decryption using ' + str(enc_dec) +
          "  Expected " + str(plaintext)  + ", got " +
          str(decryptedtext) )

  def assert_save_to_file(self, text):
    plaintext = text
    for i, enc_dec in enumerate(self.enc_decs):
      enc_dec.set_key(enc_dec.generate_key(None))
      ciphertext = enc_dec.encrypt(plaintext)
      enc_dec.dump_key(".testkey.temp")
      other_enc_dec = self.other_enc_decs[i]
      other_enc_dec.load_key(".testkey.temp")
      decryptedText = other_enc_dec.decrypt(ciphertext)
      self.assertEqual(text, decryptedText, 'incorrect decryption ' +
      'after loading key from file using ' + str(enc_dec))


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

  def test_file_hello(self):
    """
    Most basic test.  Just encrypts hello and sees
    if it is able to decrypt back.
    """
    self.assert_save_to_file("hello")

  def test_file_complete(self):
    """
    Test all the availible symbol set
    """
    self.assert_save_to_file("abcdefghijklmnopqrstuvwxyz.,!? ")

  def test_file_double_complete(self):
    """
    Test all the availible symbol set twice.  This might help test
    polyalphabetic of stream siphers
    """
    self.assert_save_to_file("abcdefghijklmnopqrstuvwxyz.,!? " * 2)

  def test_file_triple_complete(self):
    """
    Same reasoning as test_double_complete
    """
    self.assert_save_to_file("abcdefghijklmnopqrstuvwxyz.,!? " * 3)


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

class PackerTestCase(unittest.TestCase):
  def setUp(self):
    self.p = encdec.Packer()

  def test_basic_packing(self):
    plaintext = "hello"
    packed_bytes = self.p.pack(plaintext)
    unpacked_bytes = self.p.unpack(packed_bytes)
    self.assertEqual(unpacked_bytes, "hello")

  def test_full_packing(self):
    plaintext = "abcdefghijklmnopqrstuvwxyz.,!? " * 3
    packed_bytes = self.p.pack(plaintext)
    unpacked_bytes = self.p.unpack(packed_bytes)
    self.assertEqual(unpacked_bytes, plaintext)


  def tearDown(self):
    self.p = None

class PackingAndConvertingTestCase(unittest.TestCase):
  def setUp(self):
    self.p = encdec.Packer()

  def test_packing_and_converting(self):
    string = "abcdefghijklmnopqrstuvqxyz,.? "
    packed_string = self.p.pack(string)
    longval, length = util.byte_string_to_long(packed_string)
    packed_again_string = util.long_to_byte_string(longval, length)
    unpacked_string = self.p.unpack(packed_again_string)
    self.assertEqual(string, unpacked_string, string + " and " + unpacked_string + " are not equal!")

class PolygramTestCase(unittest.TestCase):
  def setUp(self):
    self.p = encdec.Polygram()

  def assert_different_block_sizes(self, plaintext):
    for i in range(1, 19):
      self.p.set_key(self.p.generate_key(i))
      ciphertext = self.p.encrypt(plaintext)
      decrypted_ciphertext = self.p.decrypt(ciphertext)
      self.assertEqual(plaintext, decrypted_ciphertext, 'Failed polygram decryption ' +
          'with different block sizes!')

  def test_hello_different_block_sizes(self):
    plaintext = "hello"
    self.assert_different_block_sizes(plaintext)

  def test_complete_different_block_sizes(self):
    """
    Test all the availible symbol set
    """
    self.assert_different_block_sizes("abcdefghijklmnopqrstuvwxyz.,!? ")

  def test_double_complete_different_block_sizes(self):
    """
    Test all the availible symbol set twice.  This might help test
    polyalphabetic of stream siphers
    """
    self.assert_different_block_sizes("abcdefghijklmnopqrstuvwxyz.,!? " * 2)

  def test_triple_complete_different_block_sizes(self):
    """
    Same reasoning as test_double_complete
    """
    self.assert_different_block_sizes("abcdefghijklmnopqrstuvwxyz.,!? " * 3)
    
  def test_hello_no_packing(self):
    plaintext = "hello"
    self.p.disable_packing()
    self.assert_different_block_sizes(plaintext)

  def test_complete_no_packing(self):
    """
    Test all the availible symbol set
    """
    self.p.disable_packing()
    self.assert_different_block_sizes("abcdefghijklmnopqrstuvwxyz.,!? ")

  def test_double_complete_no_packing(self):
    """
    Test all the availible symbol set twice.  This might help test
    polyalphabetic of stream siphers
    """
    self.p.disable_packing()
    self.assert_different_block_sizes("abcdefghijklmnopqrstuvwxyz.,!? " * 2)

  def test_triple_complete_no_packing(self):
    """
    Same reasoning as test_double_complete
    """
    self.p.disable_packing()
    self.assert_different_block_sizes("abcdefghijklmnopqrstuvwxyz.,!? " * 3)


if __name__ == "__main__":
  unittest.main()
