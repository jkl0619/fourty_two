#!/usr/bin/env python3

import sys
import os
import time
import socket
from serverKeys import getKey
from gtts import gTTS
import wolframalpha

if len(sys.argv) == 6:
	#Create Socket:
	host = ''
	port = sys.argv[2]
	backlog = sys.argv[4]
	size = sys.argv[6]
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host,port))
	print('[Checkpoint] Created socket at ' + s.host.text + ' on port ' + s.port.text)

	#Wait for connection:
	print('[Checkpoint] Listening for client connections')
	s.listen(backlog)
	
	#Check if client has connected:
	client, client_address = s.accept()		
	print('[Checkpoint] Accepted client connection from ' + client_address + ' on port ' + client.port)
	
	#Receive Data:
	payload_recieve = client.recv(size)
	client.close()
	print('[Checkpoint] Received data: ' + payload_receive)
	
	#Make sure checksum is valid:
	print('[Checkpoint] Checksum is ' + checksum_bool)

	#Do decription
	print('[Checkpoint] Decrypt: Using Key: ' + key_de + ' | ' + 'Plaintext: ' + question_plain)
	
	#TTS played out loud
	tts = gTTS(text=question_plain, lang='en', slow=False)		#convert answer into google's text to speech data type
	tts.save("question.mp3")							#save the tts file 
	os.system(oxmplayer question.mp3)					#play the mp3 file
	print('[Checkpoint] Speaking: ' + question_plain)
	
	#Send question to Wolfram Alpha
	client = wolframalpha.Client(wolfram_key)
	print('[Checkpoint] Sending question to Wolfram Alpha: ' + question_plain)
	
	#Receive answer from Wolfram Alpha
	res =  client.query(quest)
	answer_plain = next(res.results).text
	print('[Checkpoint] Received answer from Wolfram Alpha: ' + answer_plain)
	
	#Encrypt the answer
	print('[Checkpoint] Encrypt: Generated Key: ' + key_en + ' | ' + 'Ciphertext: ' answer_crypt)
	
	#Generate MD5 checksum
	print('[Checkpoint] Generated MD5 Checksum: ' + checksum_en)
	
	#Send the data
	print('[Checkpoint] Sending data: ' + payload_send)
	
	quest = input("What is your question?\n")

	wolfram_key = getKey()

	try:		   
		
		
		
		
		print(answer)

		

	except:
			print("Misinterpreted question, or unable to give good answer.")

else:
	print('Invalid commmand line inputs')
	



