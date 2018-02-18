#!/usr/bin/env python3

import sys
import os
import hashlib
import socket
import pickle
from cryptography.fernet import Fernet
from serverKeys import getKey
from gtts import gTTS
import wolframalpha


if len(sys.argv) == 7: 
        #Create Socket:
        host = ''
        port = int(sys.argv[2])
        backlog = int(sys.argv[4])
        size = int(sys.argv[6])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host,port))
        print('[Checkpoint] Created socket at ' + socket.gethostbyname(host) + ' on port ' + str(port))

        #Wait for connection:
        print('[Checkpoint] Listening for client connections')
        s.listen(backlog)
        
        #Check if client has connected:
        Client_tuple = s.accept()
        print('[Checkpoint] Accepted client connection from ' + str(Client_tuple[1][0]) + ' on port ' + str(Client_tuple[1][1]))
        
        while 1:
            #Receive Data:
            payload_receive = Client_tuple[0].recv(size)
            while (payload_receive == b''):
                payload_receive = Client_tuple[0].recv(size)
            print('[Checkpoint] Received data: %s' % payload_receive)
            
            #Make sure checksum is valid:
            payload_unpickled = pickle.loads(payload_receive)
            key_de = payload_unpickled[0]
            question_encrypted = payload_unpickled[1]
            question_checksum = payload_unpickled[2]
            n = hashlib.md5()
            n.update(question_encrypted)
            checksum_test = n.hexdigest()
            checksum_bool = 'INVALID'
            if checksum_test == question_checksum:
                checksum_bool = 'VALID'
            if checksum_bool == 'INVALID':
                print('Invald checksum')
                Client_tuple[0].close()
                s.shutdown(SHUT_WR)
                sys.exit()
            print('[Checkpoint] Checksum is ' + checksum_bool)

            #Do decryption
            key_de_fernet = Fernet(key_de)
            question_plain = key_de_fernet.decrypt(question_encrypted)
            question_plain = question_plain.strip()
            question_plain = question_plain.decode('utf-8').replace('\n', ' ')
            print('[Checkpoint] Decrypt: Using Key: %s | Plaintext: %s' % (key_de , question_plain))
            
            #TTS played out loud
            tts = gTTS(text=question_plain, lang='en', slow=False)		#convert answer into google's text to speech data type
            tts.save("question.mp3")							#save the tts file 
            os.system("omxplayer question.mp3")					#play the mp3 file
            print('[Checkpoint] Speaking: ' + question_plain)
            
            #Send question to Wolfram Alpha
            wolfram_key = getKey()
            client = wolframalpha.Client(wolfram_key)
            print('[Checkpoint] Sending question to Wolfram Alpha: ' + question_plain)
            
            try:
                #Receive answer from Wolfram Alpha
                res =  client.query(question_plain)
                answer_plain = next(res.results).text
                print('[Checkpoint] Received answer from Wolfram Alpha: ' + answer_plain)
            except ValueError:
                print('Wolfram Alpha struggled to answer the question.')
            
            #Encrypt the answer
            key_en = Fernet.generate_key()
            f = Fernet(key_en)
            answer_crypt = f.encrypt(answer_plain.encode('utf-8'))
            print('[Checkpoint] Encrypt: Generated Key: %s | Ciphertext: %s' % (key_en, answer_crypt))
            
            #Generate MD5 checksum
            m = hashlib.md5()
            m.update(answer_crypt)
            checksum_en = m.hexdigest()
            print('[Checkpoint] Generated MD5 Checksum: ' + checksum_en)
            
            #Send the data
            payload_send = pickle.dumps((key_en, answer_crypt, checksum_en))
            Client_tuple[0].send(payload_send)
            print('[Checkpoint] Sending data: %s' % payload_send)
            print('\n\n')
else:
        print("Invalid command line inputs")
    




