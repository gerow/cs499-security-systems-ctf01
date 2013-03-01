#!/usr/bin/python

import sys
import os

class EncryptorDecryptor(object):
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

  def encrypt_stdin_to_stdout(self):
    """
    Just use this encryption method to encrypt lines from stdin
    and print them to stdout
    """
    for l in sys.stdin:
      l = l.strip()
      print self.encrypt(l)

  def decrypt_stdin_to_stdout(self):
    """
    Decrypt the values on stdin and print them to stdout
    """
    for l in sys.stdin:
      l = l.strip()
      print self.decrypt(l)

  def run_from_command_line_to_dir(self, from_dir, to_dir):
    dirs = os.listdir(from_dir)
    dirs.sort()
    for fn in dirs:
      print "Encrypting " + fn
      with open(os.path.join(from_dir, fn), "r") as r:
        with open(os.path.join(to_dir, fn), "w") as w:
          w.write(self.encrypt(r.read().strip("\n")))

  def run_from_command_line(self):
    """
    Run this using arguments from the command line.  The args are
    as follows:
    arg1 is either e or d and determines whether we are encrypting
    or decrypting
    arg2 is the filename for the key we want to load
    """
    self.load_key(sys.argv[2])
    if sys.argv[1] == "e":
      self.encrypt_stdin_to_stdout()
    elif sys.argv[1] == "dir":
      self.run_from_command_line_to_dir(sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "d":
      self.decrypt_stdin_to_stdout()
    else:
      print "invalid action (must use e to encrypt or d to decrypt)"

# Import monoalphabetic to be a part of this package
from encdec_monoalphabetic import Monoalphabetic
from encdec_pack import Packer
from encdec_polygram import Polygram
from encdec_no import No
from encdec_polyalphabetic import Polyalphabetic
from encdec_homophonic import Homophonic
from encdec_streamcipher import Stream
from encdec_fibb_lfsr import FibbLFSR
