#!/usr/bin/python

import copy
import math
import pickle
from collections import deque
import random

import util

from encdec import *

class Polygram(EncryptorDecryptor):
  """
  An EncryptorDecryptor that is able to work on
  the block level.  It can generate keys for any
  arbitrary number of bits and uses the packing
  utility in order to make these keys more effective
  at lower lengths
  @author gerow
  """
  def __init__(self):
    self.key = {}
    self.key['length'] = 0
    self.key['blocks'] = {}
    self.key['packing'] = True
    self.key['iv'] = 0
    self.inv_blocks = {}
    self.packer = Packer()
    self.block_mask = 0
    self.e_vector = 0
    self.d_vector = 0

  def set_key(self, key):
    """
    Set the key for the polygram function.  This
    is expected to be a dict with a length and dict
    named blocks that maps each block to its value
    """
    self.key = key
    self.inv_blocks = {}
    self.__build_inv_blocks()
    self.__build_block_mask()
    self.e_vector = self.key['iv']
    self.d_vector = self.key['iv']

  def __build_inv_blocks(self):
    for k, v in self.key['blocks'].iteritems():
      self.inv_blocks[v] = k

  def __build_block_mask(self):
    for i in range(self.key['length']):
      self.block_mask |= (1 << i)

  def encrypt(self, plaintext):
    # First we should pack the data
    # into a long using our packer
    if self.key['packing']:
      blocks = self.packer.pack(plaintext)
    else:
      blocks = plaintext
    l, length = util.byte_string_to_long(blocks)
    output = 0L
    shift = 0
    while shift < length:
      plain_block = (l >> shift) & self.block_mask
      cipher_block = self.__encrypt_block(plain_block)
      output |= (cipher_block << shift)
      shift += self.key['length']

    return util.long_to_byte_string(output, length)

  def __encrypt_block(self, block):
    block = (block ^ self.e_vector) & self.block_mask
    out = self.key['blocks'][block]
    self.e_vector = out
    return out

  def decrypt(self, ciphertext):
    l, length = util.byte_string_to_long(ciphertext)
    output = 0L
    shift = 0
    while shift < length:
      cipher_block = (l >> shift) & self.block_mask
      plain_block = self.__decrypt_block(cipher_block)
      output |= (plain_block << shift)
      shift += self.key['length']

    byte_string = util.long_to_byte_string(output, length)
    if self.key['packing']:
      unpacked_value = self.packer.unpack(byte_string)
    else:
      unpacked_value = byte_string
    return unpacked_value

  def __decrypt_block(self, block):
    through_block_dict = self.inv_blocks[block]
    out = (through_block_dict ^ self.d_vector) & self.block_mask
    self.d_vector = block
    return out


  def generate_key(self, args):
    """
    We expect args to be the block length in bits.  Note
    that the key size doubles for every bit we add
    """
    key = {}
    key['length'] = 0
    key['blocks'] = {}
    # Default to packing enabled
    key['packing'] = True
    if args == None:
      # Default to 9 bit blocks
      args = 9 
    key['length'] = args

    # First geneate a list of symbols
    symbols = []
    for i in range(2**key['length']):
      symbols.append(i)

    random.shuffle(symbols)
    symbols = deque(symbols)
    # Using a deque gives us O(1) pop
    # operations

    # Now randomly grab them
    for i in range(2**key['length']):
      key['blocks'][i] = symbols.pop()

    # Now randomly generate an
    # initialization vector

    key['iv'] = random.randint(0, 2**args)

    return key

  def dump_key(self, filename):
    with open(filename, "w") as f:
      pickle.dump(self.key, f)

  def load_key(self, filename):
    with open(filename, "r") as f:
      self.set_key(pickle.load(f))

  def disable_packing(self):
    self.key['packing'] = False
  
  def enable_packing(self):
    self.key['packing'] = True

if __name__ == "__main__":
  m = Polygram()
  m.run_from_command_line()
