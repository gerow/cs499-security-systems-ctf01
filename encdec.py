#!/usr/bin/python

##
# The encdec module should incldue not only the EncryptorDecryptor
# interface, but also all the actual encryption and decryption
# implementations.  This should help keep all the encryption and
# decryption stuff in once place.
##

class EncryptorDecryptor:
  ##
  # A simple interface that encryption classes should support
  
  ## # This method should allw the EncryptorDecryptor to set its key
  # in some way.  What this type is will be very different depending
  # upon the implementation.
  # @param key some type that the implementing class chooses to represent
  #     a key for its EncryptorDecryptor
  
  def set_key(key):
    raise NotImplementedError("An EncryptorDecryptor must implement set_key")

  ##
  # If given a string this method should return its encrypted form
  # @param plaintext the plaintext we wish to convert into ciphertext

  def encrypt(plaintext):
    raise NotImplementedError("An EncryptorDecryptor must implement encrypt")

  ##
  # If given a string this method should return the plaintext form.
  # @param ciphertext the ciphertext we wish to convert into plaintext
  
  def decrypt(ciphertext):
    raise NotImplementedError("An EncryptorDecryptor must implement decrypt")

  ##
  # We should be able to generate a key given some arguments.  For some
  # implementations this will likely be None, but for others it may include
  # some kind of length, and even for polyalphabetic ciphers it may include
  # the plaintext we wish to generate an optimal key for.
  # @param args the type of this value is chosen by the implementing class

  def generate_key(args):
    raise NotImplementedError("An EncryptorDecryptor must implement this")

  ##
  # Open file at the filename provided and write our key to it
  # @param filename the name of the file we wish to write our
  #     key to

  def write_key(filename):
    raise NotImplementedError("An EncryptorDecryptor must implement this")

  ##
  # The complement of write_key.  This method should read the key at the
  # filename given and start using it as this instance's key.
  # @param filename the name of the file we wish to read our key from
  
  def read_key(filename):
    raise NotImplementedError("An EncryptorDecryptor must implement this")
