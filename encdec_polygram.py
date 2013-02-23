#!/usr/bin/python

import copy
import math

import util

from encdec import *

class Polygram(EncryptorDecryptor):
  def __init__(self):
    self.key = {}
    self.key['length'] = 0
    self.key['blocks'] = {}
    self.inv_blocks = {}
    self.packer = Packer()
    self.block_mask = 0

  def set_key(self, key):
    self.key = key
    self.inv_blocks = {}
    self.__build_inv_blocks()
    self.__build_block_mask()

  def __build_inv_blocks(self):
    for k, v in self.key['blocks'].iteritems():
      self.inv_blocks[v] = k

  def __build_block_mask(self):
    for i in range(self.key['length']):
      self.block_mask |= (1 << i)

  def encrypt(self, plaintext):
    # First we should pack the data
    # into a long using our packer
    blocks = self.packer.pack(plaintext)
    l, length = util.byte_string_to_long(blocks)
    output = 0L
    shift = 0
    while shift < length:
      plain_block = (l >> shift) & self.block_mask
      cipher_block = self.key['blocks'][plain_block]
      output |= (cipher_block << shift)
      shift += self.key['length']

    return util.long_to_byte_string(output, length)

  def decrypt(self, ciphertext):
    l, length = util.byte_string_to_long(ciphertext)
    output = 0L
    shift = 0
    while shift < length:
      cipher_block = (l >> shift) & self.block_mask
      plain_block = self.inv_blocks[cipher_block]
      output |= (plain_block << shift)
      shift += self.key['length']

    byte_string = util.long_to_byte_string(output, length)
    unpacked_value = self.packer.unpack(byte_string)
    return unpacked_value

  def generate_key(self, args):
    """
    We expect args to be the block length in bits.  Note
    that the key size doubles for every bit we add
    """
    key = {}
    key['length'] = 0
    key['blocks'] = {}
    if args == None:
      # Default to 8 bit blocks
      args = 7 
    key['length'] = args

    # First geneate a list of symbols
    symbols = []
    for i in range(2**key['length']):
      symbols.append(i)

    # Now randomly grab them
    for i in range(2**key['length']):
      key['blocks'][i] = util.rand_pop(symbols)

    return key

  def dump_key(self, filename):
    pass

  def load_key(self, filename):
    pass
