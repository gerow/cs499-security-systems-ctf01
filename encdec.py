#!/usr/bin/python

import copy
import random
import pickle

class EncryptorDecryptor:
  """
  A simple interface that encryption classes should support
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

class Monoalphabetic:
  def __init__(self):
    self.__key = {}
    self.__inv_key = {}

  def __rand_pop(self, elements):
    random.shuffle(elements)
    return elements.pop(0)

  def __generate_inv_key(self):
    for key, value in self.__key.iteritems():
      self.__inv_key[value] = key

  def set_key(self, key):
    self.__key = copy.copy(key)
    self.__inv_key = {}
    self.__generate_inv_key()

  def encrypt(self, plaintext):
    out = ""
    for c in plaintext:
      out += self.__key[c]
    return out

  def decrypt(self, ciphertext):
    out = ""
    for c in ciphertext:
      out += self.__inv_key[c]
    return out
    
  def generate_key(self, args):
    # We're going to ignore the args since
    # we don't need them
    symbols = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
               "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
               "y", "z", ".", ",", "!", "?", " "]
    symbols_availible = copy.copy(symbols) 
    key = {}
    for symbol in symbols:
      key[symbol] = self.__rand_pop(symbols_availible)
    return key

  def dump_key(self, filename):
    with open(filename, "w") as f:
      pickle.dump(self.__key, f)

  def load_key(self, filename):
    with open(filename, "r") as f:
      self.__key = pickle.load(f)
    self.__generate_inv_key()
