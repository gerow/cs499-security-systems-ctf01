import random
import util
import pickle
import copy
from encdec import*

class Stream(EncryptorDecryptor):
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
         self.__inv_key = self.__key
         return self.__inv_key
         
     def set_key(self,key):
         self.__key = copy.copy(key)
         self.__inv_key = {}
         self.__generate_inv_key()

     def encrypt(self, plaintext):
         key = copy.copy(self.__key)
         ciphers = []
         for x in range(0,plaintext.__len__()*8):
               itemInsert = ((((key[0] ^ key[2]) ^ key[3]) ^ key[5]) ^ key[15])
               fallOut = key.pop()
               ciphers.append(fallOut)
               key.insert(0, itemInsert)
         out = ""
         self.__key = key
         position = plaintext.__len__() * 8 - 1
         for c in plaintext:
                 num = 0
                 for i in range(0,8):
                     num +=  ciphers[position-i] * 2 ** (7-i) 
                 position = position - 7
                 out += (chr(ord(c) ^ num))
         return out

     def decrypt(self, ciphertext):
         inv_key = copy.copy(self.__inv_key)
         deciphers = []
         for x in range(0,ciphertext.__len__()*8):
               itemInsert = ((((inv_key[0] ^ inv_key[2]) ^ inv_key[3]) ^ inv_key[5]) ^ inv_key[15])
               fallOut = inv_key.pop()
               deciphers.append(fallOut)
               inv_key.insert(0, itemInsert)
         self.__inv_key = inv_key
         out = ""
         position = ciphertext.__len__() * 8 - 1
         for c in ciphertext:
                 num = 0
                 for i in range(0,8):
                     num +=  deciphers[position-i] * 2 ** (7-i) 
                 position = position - 7
                 out += (chr(ord(c) ^ num))
         return out

     def generate_key(self, args): 
         key = []
         for i in range(0,16):
             key.append(random.randint(0,1))
         
         return key


     def dump_key(self, filename):
         with open(filename, "w") as f:
             pickle.dump(self.__key, f)
         
     def load_key(self, filename):
         with open(filename, "r") as f:
             self.__key = pickle.load(f)
         self.__generate_inv_key()

