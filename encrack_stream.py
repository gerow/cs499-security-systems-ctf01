import sys

import encdec
import util
import copy
import random

from encrack import*

class Stream (EncryptionCracker):
    def __init__(self, directory):
        super(Stream,self).__init__(directory)
        self.a = Analysis()
        self.e = encdec.Stream()
        self.d = Dictcheck()
        self.key = []
        self.__init_key()
        self.key_stack = []

    def __init_key(self):
        for i in range (16):
            self.key.append(0)

    def push_key(self):
        self.key_stack.append(copy.copy(self.key))

    def pop_key(self):
        self.key = self.key_stack.pop()

    def clear_key_stack(self):
        self.key_stack =[]

    def decrypt(self):
        self.e = encdec.Stream()
        self.e.set_key(self.key)
        out = []
        for m in self.messages:
            out.append(self.e.decrypt(m))
        return out

    def score(self):
        chars_in_dict = self.a.fraction_chars_in_dict(self.decrypt())
        return chars_in_dict

    def remove_normal_punc(self, word):
        if word[-1] in (".",",","!","?"):
            return word[:-1]
        return word

    def brute_force_crack(self):
        self.load_new_messages()
        best_score = 0.0
        best_key = []
        best_decrpyt = ""
        print "MESSAGES: " + str(self.messages)
        for i in range (1,65536):
            cout = self.key[0]
            self.key[0] = (self.key[0] + 1) % 2
            for v in range (1,16):
                if cout == 1:
                    cout = self.key[v]
                    self.key[v] = (self.key[v] + 1) % 2    
                else:
                    self.key[v] = self.key[v]
                    cout = 0
            decrypted = self.decrypt()
            if self.score() > best_score:
                best_key = self.key
                best_score = self.score()
                best_decrypt = decrypted
                print best_score
                print decrypted
            if self.score() == 1.0:
                print decrypted
                best_key = self.key
                best_score = self.score()
                best_decrypt = decrypted

                return
            
        print str(best_decrpyt)
    def crack(self):
        self.brute_force_crack()

if __name__ == "__main__":
  directory = sys.argv[1]
  s = Stream(directory)
  s.crack()
  
