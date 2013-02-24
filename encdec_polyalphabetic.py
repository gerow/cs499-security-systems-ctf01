#!/usr/bin/python

import copy
import random
import collections
import pickle

import util

from encdec import *

class Polyalphabetic(EncryptorDecryptor):
  """
  Class that implements polyalphabetic encryptor
  and decryptor
  """

  def __init__(self):
    self.__key = []
    self.__inv_key = []
    self.__enc_num = 0
    self.__dec_num = 0

  def __generate_inv_key(self):
    self.__inv_key = []
    for alphabet in self.__key:
      inv_alphabet = {}
      for key, value in alphabet.iteritems():
        inv_alphabet[value] = key
      self.__inv_key.append(inv_alphabet)

  def set_key(self, key):
    """
    Set our key to the new value and generate
    our inverse key
    """
    self.__key = key
    self.__generate_inv_key()

  def __encrypt_char(self, char):
    """
    Encrypt a single character and increment our
    enc counter so we move to the next alphabet
    """
    out = self.__key[self.__enc_num][char]
    self.__enc_num = (self.__enc_num + 1) % len(self.__key)
    return out

  def encrypt(self, plaintext):
    """
    For each character call the next alphabet to
    encrypt and so on
    """
    out = ""
    for c in plaintext:
      out += self.__encrypt_char(c)
    return out

  def __decrypt_char(self, char):
    """
    Much like encrypt_char, except we use the
    inverse key
    """
    out = self.__inv_key[self.__dec_num][char]
    self.__dec_num = (self.__dec_num + 1) % len(self.__key)
    return out

  def decrypt(self, plaintext):
    out = ""
    for c in plaintext:
      out += self.__decrypt_char(c)
    return out

  def __generate_alphabet(self):
    """
    Generate a single alphabet
    """
    symbols = list(util.SYMBOLS)
    random.shuffle(symbols)
    symbol_pool = collections.deque(symbols)

    alphabet = {}

    for symbol in util.SYMBOLS:
      alphabet[symbol] = symbol_pool.pop()

    return alphabet

  def generate_key(self, args):
    """
    Args is expected to be a number
    indicating the number of alphabets
    """
    if args == None:
      args = 20
    num_alphabets = args
    key = []
    for i in range(num_alphabets):
      key.append(self.__generate_alphabet())

    return key

  def dump_key(self, filename):
    with open(filename, "w") as f:
      pickle.dump(self.__key, f)

  def load_key(self, filename):
    with open(filename, "r") as f:
      self.set_key(pickle.load(f))
