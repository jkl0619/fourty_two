#!/usr/bin/env python3


# """A simple echo client"""
import socket
import tweepy
from clientKeys import *
import optparse
import hashlib, pickle
from cryptography.fernet import Fernet
from gtts import gTTS
import os
import sys

# -s ip -p port -z size -t hashtag
# Parse through the arguments
parser = optparse.OptionParser()
parser.add_option('-s', dest='host', help='The host ip address to connect the client to')
parser.add_option('-p', dest='port', help='The port to connect to')
parser.add_option('-z', dest='size', help='The size')
parser.add_option('-t', dest='hashtag', help='The hashtag to filter')
(options, args) = parser.parse_args()

# initialize values from command line
host = options.host
port = int(options.port)
size = int(options.size)
hashtag = options.hashtag
print("[Checkpoint] Listening for Tweets that contain: " + hashtag)
hashtag = hashtag.strip()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set consumer token + access token
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# generate fernet key

s.connect((host, port))
api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        messages = status.text
        user = status.user.name
        key = Fernet.generate_key()
        print("[Checkpoint] New Tweet: " + messages + " | User: " + user)
        filteredMessage = messages.replace(hashtag, '')  # Gets rid of hashtag in the message
        f = Fernet(key)
        token = f.encrypt(filteredMessage.encode('utf-8'))  # ciphered text
        print("[Checkpoint] Encrypt: Generated Key: %s" % key)
        print("| Ciphertext: %s" % token)
        m = hashlib.md5()
        m.update(token)
        checksum = m.hexdigest()
        print("[Checkpoint] Generated MD5 Checksum: " + checksum)
        pickleCheckSum = pickle.dumps((key, token, checksum))
        print("[Checkpoint] Connecting to %s on port %s" % (host, port))

        s.send(pickleCheckSum)  # bytes

        print("[Checkpoint] Sending data %s" % pickleCheckSum)
        data_tuple = s.recv(size)
        print("[Checkpoint] Received data %s" % data_tuple)
        payload_unpickle = pickle.loads(data_tuple)
        key_de = payload_unpickle[0]
        answer_enc = payload_unpickle[1]
        answer_checksum = payload_unpickle[2]
        n = hashlib.md5()
        n.update(answer_enc)
        checksum_test = n.hexdigest()
        checksum_bool = 'INVALID'
        if checksum_test == answer_checksum:
            checksum_bool = 'VALID'
        if checksum_bool == 'INVALID':
            sys.exit()
        print('[Checkpoint] Checksum is ' + checksum_bool)

        key_de_fernat = Fernet(key_de)
        answer_plain = key_de_fernat.decrypt(answer_enc).decode('utf-8')
        print('[Checkpoint] Decrypt: Using key: %s | Plaintext: %s' % (key_de, answer_plain))

        tts = gTTS(text=answer_plain, lang='en', slow=False)
        tts.save("answer.mp3")
        os.system("omxplayer answer.mp3")
        print('[Checkpoint] Speaking: ' + answer_plain)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=[hashtag])