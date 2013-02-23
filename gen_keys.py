#!/usr/bin/python

import encdec

def generate_keys():
  # First, let's make a monoalphabetic cipher
  e = encdec.Monoalphabetic()
  e.set_key(e.generate_key(None))
  e.dump_key("keys/ma.key")

  # Now let's make a large polygram key with packing
  e = encdec.Polygram()
  e.set_key(e.generate_key(23))
  e.dump_key("keys/pg.key")

  # Now turn off packing
  e.disable_packing()
  e.dump_key("keys/pg_nopacking.key")

if __name__ == "__main__":
  generate_keys()
