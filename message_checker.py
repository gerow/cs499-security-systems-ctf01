import sys
import enchant

class MessageChecker:

	"""
	This class will take a create a dictionary lookup table
	upon instantiation.  Then, provided with a text string,
	it will return a score between 0 and 1 determining how
	likely the string is a readable English language sentence.
	"""

	def __init__(self, textfile):
		with open(textfile, 'r') as f:
			tempList = []
			for line in f:
				tempList.append(line.strip())
			self.lookupTable = frozenset(tempList)
		
	def score (self, string):
		words = string.split()
		numWords = 0
		for word in words:
			if word.strip('.?! ') in self.lookupTable:
				numWords+=1
		return float(numWords) / len(words)

	def score2 (self, string):
		words = string.split()
		numWords = 0
		d = enchant.Dict("en_US")
		for word in words:
			if word.strip('.?! ') in d:
				numWords += 1
		return float(numWords) / len (words) 
if __name__ == "__main__":
	messageChecker = MessageChecker("words.txt")
	print messageChecker.score2(sys.argv[1])
	pass
