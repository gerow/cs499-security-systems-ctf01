
import nfqueue
import cracker
import thread
#from scapy.all import IP, TCP,
import socket
import time
from dpkt import ip, tcp, hexdump, udp


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

count = 0
def crack(dummy, payload):
	global count
	print "Got packet"
	data = payload.get_data()
	packet = ip.IP(data)
	#print packet.tcp.data
	#print payload[TCP]
	print packet.p == ip.IP_PROTO_TCP
	mData = ""
	if packet.p == ip.IP_PROTO_TCP:
		mData = packet.tcp.data
	elif packet.p == ip.IP_PROTO_UDP:
		mData = packet.udp.data
	
	if len(mData) != 0:
		outFileName = str(packet.tcp.dport) + "_id" + str(count)
		fout = open(outFileName, 'wb')
		print mData
		fout.write(mData)
		fout.close()
		count = count + 1
	payload.set_verdict(nfqueue.NF_ACCEPT)
	

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



