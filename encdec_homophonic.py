import random
import util
import pickle
import copy
from encdec import*

class Homophonic(EncryptorDecryptor):
     """
     Implemtation of EncryptorDecryptor that provides homophonic ciphers
     @author jiachenz
     """
     def __init__(self):
          """
          Init empty keys
          """
          self.__key = {}
          self.__inv_key ={}
          
     def __generate_inv_key(self):
          """
          Generate the inverse key to decrypt
          """
   
          for k,v in self.__key.iteritems():
               for num in v:
                    self.__inv_key[int(num)] = k
          return self.__inv_key
         
     def set_key(self, key):
          self.__key = copy.copy(key)
          self.__inv_key = {}
          self.__generate_inv_key()

     def encrypt(self, plaintext):
          out = ""
          keys = copy.copy(self.__key)
          for c in plaintext:
               out += str(keys[c][random.randrange(0,len(keys[c]))])
          return out
         
     def decrypt(self, ciphertext):
          out = ""
          inv_key = copy.copy(self.__inv_key)
          pos = 0
          while (pos <= len(ciphertext)-1):
               numString = ""
               for i in range(0,3):
                    numString +=(ciphertext[pos + i])
               num = int(numString)
               out += inv_key[num]
               pos += 3
          return out
         
     def generate_key(self, args): 
          symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                    'y', 'z', '.', ',', '!', '?', ' ']
          ciphers = []
          key = {}
          for i in range(100,1000):
               ciphers.append(i)
          occurrences = { 'a':8,'b':2, 'c':3, 'd':4, 'e':12, 'f':2, 'g':2, 'h':6, 'i':6, 'j':1, 'k':1, 'l':4,
                    'm':2, 'n':6, 'o':7, 'p':2, 'q':1, 'r':6, 's':6, 't':8, 'u':3, 'v':1, 'w':2, 'x':1,
                    'y':2, 'z':1, '.':6,',':5, '!':1, '?':1, ' ':10}
          for symbol in symbols:
               key[symbol] = list()
               for i in range(0, occurrences[symbol]):
                    key[symbol].append(util.rand_pop(ciphers))
          return key


     def dump_key(self, filename):
          with open(filename, "w") as f:
               pickle.dump(self.__key, f)
         
     def load_key(self, filename):
          with open(filename, "r") as f:
               self.__key = pickle.load(f)
          self.__generate_inv_key()

