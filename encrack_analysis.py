#!/usr/bin/python

import encrack

class Analysis:
  def __init__(self):
    self.d = encrack.Dictcheck()

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

  def detect_odd_space(self, messages):
    """
    Return a list of indicies for each
    message if we detect odd spaces.  That
    includes spaces at the beginning or end
    of the message or multiple spaces next to
    each other. In the case of multiple spaces
    next to each other we list the index of the
    first instance unless we have three spaces
    in which case we list the first two and so on
    """
    problems = []
    for i, message in enumerate(messages):
      # Create a new entry for this message
      problems.append([])
      # Ignore message if empty
      if not message:
        continue
      if message[0] == " ":
        problems[i].append(0)
      for j, c in enumerate(message):
        try:
          if c == " " and message[j + 1] == " ":
            problems[i].append(j)
        except IndexError:
          # Just ignore it, we're cool
          pass
      if message[-1] == " ":
        problems[i].append(len(message) - 1)
    # Return an empty list if it is nothing but
    # empty list (so this can be used with an if
    # statement)

    for message_problem in problems:
      if message_problem:
        return problems
    return []

  def fraction_chars_in_dict(self, messages):
    """
    Works much like the one in dictcheck except it
    operates on an array of messages
    """
    output = 0.0
    count, counts = self.__count_letters(messages)
    total_len = count

    for i, m in enumerate(messages):
      weight = float(counts[i])/total_len
      output += self.d.fraction_chars_in_dict(m) * weight

    return output
  
  def __count_letters(self, messages):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i","j",
               "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
               "u", "v", "w", "x", "y", "z"]
    count = 0
    counts = []
    for m in messages:
      strcount = 0
      for c in m:
        if c in letters:
          count += 1
          strcount += 1
      counts.append(strcount)
    return count, counts
