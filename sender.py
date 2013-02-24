#!/usr/bin/python

from socket import *
import sys

import util

if __name__ == "__main__":
  if len(sys.argv) != 5:
    print "usage ./sender.py hostname port encryption_type key_file"

  hostname = sys.argv[1]
  port = int(sys.argv[2])
  encryption_type = sys.argv[3]
  key_file = sys.argv[4]

  print "attempting to load encryption/decryption module and key..."
  e = util.load_encdec(encryption_type, key_file)
  print "succeded loading encryption/decryption module!"

  print "creating socket and connecting to host..."
  cli = socket(AF_INET, SOCK_STREAM)
  cli.connect(((hostname, port)))
  print "connected!"
  sequence_number = 0

  while True:
    try:
      message = raw_input("message: ")
    except EOFError:
      print "goodbye"
      break
    except KeyboardInterrupt:
      print "goodbye"
      break
    if not util.string_contains_valid_symbols(message):
      print "invalid symbols detected in message, they have been stripped or coerced to lower case"
      message = util.strip_invalid_symbols(message)
    encrypted_message = e.encrypt(message)
    cli.send(str(sequence_number) + "|" + encrypted_message)
