#!/usr/bin/python

import os

class EncryptionCracker(object):
  """
  A base class that encryption crackers should implement.
  The main thing it does is provide a way to seamlessly work
  with a directory of files each containing messages.  By simply
  calling self.load_new_messages the inheriting class can load
  any new messages in the directory into its messages array. This
  should allow new messages to be added to a cracking instance
  in process
  """
  def __init__(self, directory):
    self.messages = []
    self.directory = directory
    self.seen_files = set()
    self.load_new_messages()

  def load_new_messages(self):
    """
    This method should be called by the
    inheriting class.  It checks its set
    directory for new messages and adds
    them to the self.massages list
    Returns a list of files added so that
    the algorithm can do initialization stuff
    on the messages if needed
    """
    try:
      filenames = os.listdir(self.directory)
      files_to_add = []
      for filename in filenames:
        if filename not in self.seen_files:
          self.seen_files.add(filename)
          path = os.path.join(self.directory, filename)
          with open(path, "r") as f:
            filestring = f.read()
          files_to_add.append([filestring, filename])
      # Sort the list by mtime (using lambda!)
      files_to_add.sort(key=lambda tup: tup[1])
      print "Sorted files to add: " + str(files_to_add)
      for filestr in files_to_add:
        if filestr[0][-1] == "\n":
          filestr[0] = filestr[0][:-1]
        self.messages.append(filestr[0])
      return files_to_add
    except OSError, IOError:
      # We weren't able to read the file for some
      # reason.  Go ahead an ignore this for now
      return []

  def crack(self):
    """
    Basically, just run the cracker
    """
    raise NotImplementedError("An encryptoin cracker must implement the crack method")

from encrack_dictcheck import Dictcheck
from encrack_analysis import Analysis
