import nfqueue
import cracker
import thread

""" Modulethat will lift messages off the network
for decryption
"""
def crack():
	message = "HI"
	try:
		thread.start_new_thread(cracker.monoAlphabeticCrack, (message,))
	except:
		print "Wee"

if __name__ == "__main__":
	crack()
	"""
	q = nfqueue.queue()
	q.open()
	q.bind(socket.AF_INET)
	q.set_callback(crack)
	q.create_queue(0)

	try:
		jfjfjfjiejwiaj
	"""
"""
def crack(dummy, payload):
	try:
		thread.start_new_thread(cracker.monoAlphabeticCrack)
"""

