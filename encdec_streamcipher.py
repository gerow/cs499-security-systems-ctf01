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
	self.__inv_key = self.__key
	return self.__inv_key
	
def set_key(self key):
	self.__key = copy.copy(key)
	self.__inv_key = {}
	self.__generate_inv_key()

def encrypt(self, plaintext):
	out = ""
	position = plaintext.__len__() * 8 - 1
	for c in plaintext:
            for i in range(0,8):
                num +=  self.__key[position-i] * 2 ** (7-i) 
            position = position - 7
            out.append(chr(ord(c) ^ num))
        return out

def decrypt(self, ciphertext):
        out = ""
	position = ciphertext.__len__() * 8 - 1
	for c in ciphertext:
            for i in range(0,8):
                num +=  self.__inv_key[position-i] * 2 ** (7-i) 
            position = position - 7
            out.append(chr(ord(c) ^ num))
        return out

def generate_key(self, args): 
	shift_register = {}
	for i in range(0,15):
		shift_register.append(random.randint(0,1))
	for x in range(0,ciphertext.__len__()*8):
	    itemInsert = shift_regsiter[0] ^ shift_register[2]
	    itemInsert = itemInsert ^ shift_register[3]
	    itemInsert = itemInsert ^ shift_register[5]
	    itemInsert = itemInsert ^ shift_register[15]
	    out = shift_register.pop()
	    key.append(out)
	    shift.register.insert(0, itemInsert)
	return key


def dump_key(self, filename):
	with open(filename, "w") as f:
		pickle.dump(self.__key, f)
	
def load_key(self, filename):
	with open(filename, "r") as f:
            self.__key = pickle.load(f)
        self.__generate_inv_key()

