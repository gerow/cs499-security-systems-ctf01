#!/usr/bin/python

import copy
import random
import pickle

import util

from encdec import *

class Monoalphabetic(EncryptorDecryptor):
  """
  Implemtation of EncryptorDecryptor that provides monoalphabetic ciphers
  @author gerow
  """
  def __init__(self):
    """
    Init only initializes an empty key and empty reverse key
    """
    self.__key = {}
    self.__inv_key = {}

  def __generate_inv_key(self):
    """
    Generate the inverse key so that we can decrypt
    """
    for key, value in self.__key.iteritems():
      self.__inv_key[value] = key

  def set_key(self, key):
    """
    Set our key to the key given.  This method expects a dict
    that maps all the availible symbols to some other availible symbol
    """
    self.__key = copy.copy(key)
    self.__inv_key = {}
    self.__generate_inv_key()

  def encrypt(self, plaintext):
    """
    Encrypt the given plaintext using the key we have stored
    """
    return ''.join([self.__key[c] for c in plaintext])

  def decrypt(self, ciphertext):
    """
    Decrypt the plaintext using the inv_key we have stored
    """
    return ''.join([self.__inv_key[c] for c in ciphertext])
    
  def generate_key(self, args):
    """
    Generate a random key
    """
    # We're going to ignore the args since
    # we don't need them
    symbols = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
               "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
               "y", "z", ".", ",", "!", "?", " "]
    symbols_availible = copy.copy(symbols) 
    key = {}
    for symbol in symbols:
      key[symbol] = util.rand_pop(symbols_availible)
    return key

  def dump_key(self, filename):
    """
    Write our dict to the file given using pickle
    """
    with open(filename, "w") as f:
      pickle.dump(self.__key, f)

  def load_key(self, filename):
    """
    Read our dict from the file provided using pickle
    """
    with open(filename, "r") as f:
      self.__key = pickle.load(f)
    self.__generate_inv_key()

if __name__ == "__main__":
  m = Monoalphabetic()
  m.run_from_command_line()
