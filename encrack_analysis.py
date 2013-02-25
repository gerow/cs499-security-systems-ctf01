#!/usr/bin/python

class Analysis:
  def __init__(self):
    pass

  def frequency_report(self, messages):
    """
    Assume messages is a list of strings
    Return a dict listing each character
    in the messages and the fraction of
    the total message that it is a part of
    """
    out = {}
    for message in messages:
      for c in message:
        try:
          out[c] += 1
        except KeyError:
          out[c] = 1
    total_len = 0
    for message in messages:
      total_len += len(message)
    for k,v in out.iteritems():
      out[k] = float(v)/float(total_len)
    return out
