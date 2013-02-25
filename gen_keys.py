#!/usr/bin/python

import encdec

def generate_keys():
  # First, let's make a monoalphabetic cipher
  e = encdec.Monoalphabetic()
  e.set_key(e.generate_key(None))
  e.dump_key("keys/ma.key")

  # Now let's make a large polygram key with packing
  e = encdec.Polygram()
  e.set_key(e.generate_key(15))
  e.dump_key("keys/pg.key")

  # Now turn off packing
  e.disable_packing()
  e.dump_key("keys/pg_nopacking.key")

  # Now let's generate a polyalphabetic key
  # with 1000 alphabets
  e = encdec.Polyalphabetic()
  e.set_key(e.generate_key(1000))
  e.dump_key("keys/pa.key")

  # Ok, now make a stream cipher key
  e = encdec.Stream()
  e.set_key(e.generate_key(None))
  e.dump_key("keys/st.key")

  # Great, finally make a homophonic key
  e = encdec.Homophonic()
  e.set_key(e.generate_key(None))
  e.dump_key("keys/hp.key")

if __name__ == "__main__":
  generate_keys()
