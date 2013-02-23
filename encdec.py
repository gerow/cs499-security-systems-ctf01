#!/usr/bin/python

class EncryptorDecryptor:
  """
  A simple interface that encryption classes should support
  @author gerow
  """
  
  def set_key(self, key):
    """
    This method should allw the EncryptorDecryptor to set its key
    in some way.  What this type is will be very different depending
    upon the implementation.
    """
    raise NotImplementedError("An EncryptorDecryptor must implement set_key")

  def encrypt(self, plaintext):
    """
    If given a string this method should return its encrypted form
    """
    raise NotImplementedError("An EncryptorDecryptor must implement encrypt")
  
  def decrypt(self, ciphertext):
    """
    If given a string this method should return the plaintext form.
    """
    raise NotImplementedError("An EncryptorDecryptor must implement decrypt")

  def generate_key(self, args):
    """
    We should be able to generate a key given some arguments.  For some
    implementations this will likely be None, but for others it may include
    some kind of length, and even for polyalphabetic ciphers it may include
    the plaintext we wish to generate an optimal key for.  We should always
    have a default that we generate for when args == None
    """
    raise NotImplementedError("An EncryptorDecryptor must implement this")

  def dump_key(self, filename):
    """
    Open file at the filename provided and write our key to it
    """
    raise NotImplementedError("An EncryptorDecryptor must implement this")
  
  def load_key(self, filename):
    """
    The complement of write_key.  This method should read the key at the
    filename given and start using it as this instance's key.
    """
    raise NotImplementedError("An EncryptorDecryptor must implement this")

# Import monoalphabetic to be a part of this package
from encdec_monoalphabetic import Monoalphabetic
from encdec_pack import Packer
from encdec_polygram import Polygram
