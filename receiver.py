#!/usr/bin/python

# argument form:
# ./receiver.py port encryption_type key_file

from socket import *
import sys

import util
import encdec

HOST = ""
BUFSIZE = 8192

if __name__ == "__main__":
  if len(sys.argv) != 4:
    print "usage: ./receiver.py port encryption_type key_file"

  port = int(sys.argv[1])
  encryption_type = sys.argv[2]
  key_file = sys.argv[3]

  print "attempting to load encryption/decryption module and key..."
  e = util.load_encdec(encryption_type, key_file)
  print "succeded loading encryption/decryption module!"

  print "creating socket and binding to port"
  serv = socket(AF_INET, SOCK_STREAM)
  serv.bind(((HOST, port))) # Triple parens necessary
  print "bound to port " + str(port)
  serv.listen(5)
  print "listening..."

  conn,addr = serv.accept()
  print "...connected!"
  print "message:"
  print ""

  while True:
    data = conn.recv(BUFSIZE)
    if not data: break
    split_data = data.split("|")
    sequence_number = split_data[0]
    encrypted_data = split_data[1]
    decrypted_data = e.decrypt(encrypted_data)
    print decrypted_data

  print "remote connection closed.  closing"
  serv.close()
