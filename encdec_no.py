#!/usr/bin/python

class No:
  """
  An encdec that doesn't actually do anything.
  This ist mainly for testing purposes.
  """

  def set_key(self, key):
    pass

  def encrypt(self, plaintext):
    return plaintext

  def decrypt(self, ciphertext):
    return ciphertext

  def generate_key(self, args):
    pass

  def dump_key(self, filename):
    pass

  def load_key(self, filename):
    pass
