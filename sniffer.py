
import nfqueue
import cracker
import thread
#from scapy.all import IP, TCP
import socket
from dpkt import ip, tcp, hexdump
""" Module that will lift messages off the network
for decryption
"""
"""
def crack():
	message = "HI"
	print message
	try:
		thread.start_new_thread(cracker.monoAlphabeticCrack, (message,))
	except:
		print "W"
	while 1:
		pass
"""
def crack(dummy, payload):
	print "Got packet"
	print payload
	data = payload.get_data()
	packet = ip.IP(data)
	print packet.tcp.data
	#print payload[TCP]
	payload.set_verdict(nfqueue.NF_ACCEPT)
	"""
	try:
		thread.start_new_thread(cracker.monoAlphabeticCrack, ())
		thread.start_new_thread(cracker.polyAlphabeticCrack, ())
		thread.start_new_thread(cracker.polygramCrack, ())
		thread.start_new_thread(cracker.homophoneCrack, ())
		thread.start_new_thread(cracker.streamCrack, ())
	except:
		print "Problem with threading in sniffer.crack()
	"""

if __name__ == "__main__":
	q = None

	def cb(dummy, payload):
		print "here"
	q = nfqueue.queue()
	q.open()
	q.bind(socket.AF_INET)
	q.set_callback(crack)
	q.create_queue(0)
	
	
	try:
		q.try_run()
	except KeyboardInterrupt:
		print "Exiting"
	finally:
		q.unbind(socket.AF_INET)
		q.close()
	q.unbind(socket.AF_INET)
	q.close()



