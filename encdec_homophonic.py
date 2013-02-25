import random
import util
import key
import pickle
from encdec import*

class HomophonicAlphabet(EncryptorDecryptor):
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
     inv_key = {}
     for k,v in self.__key.iteritems():
          for num in v:
               inv_key[num] = k
     return inv_key
    
def set_key(self, key):
     self.__key = copy.copy(key)
     self.__inv_key = {}
     self.__generate_inv_key()

def encrypt(self, plaintext):
     out = ""
     keys = copy.copy(self.__key)
     for c in plaintext:
          out += str(keys[c].pop())
     return out
    
def decrypt(self, ciphertext):
     out = ""
     for pos in range(0, ciphertext.__len__()):
          numString = ""
          for i in range(0,3):
               numString = numString.append(ciphertext[pos + i])
          num = int(numString)
          out.append(self.__inv_key[num])
     return out
    
def generate_key(self, args): 
     symbols = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
               "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
               "y", "z", ".", ",", "!", "?", " "]
     ciphers = {}
     for num in range (100,1000):
          ciphers.append(num)
          symbols_availible = copy.copy(symbols) 
          key = {}
          occurrences = {}  
          for symbol in symbols:
               occurrences[symbol] = plaintext.count(symbol)
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

