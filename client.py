#!/usr/bin/env python3


# """A simple echo client"""
import socket
import tweepy
from clientKeys import *
import optparse
import hashlib, pickle
from cryptography.fernet import Fernet


# -s ip -p port -z size -t hashtag
# Parse through the arguments
parser = optparse.OptionParser()
parser.add_option('-s', dest='host', help='The host ip address to connect the client to')
parser.add_option('-p', dest='port', help='The port to connect to')
parser.add_option('-z', dest='size', help='The size')
parser.add_option('-t', dest='hashtag', help='The hashtag to filter')
(options,args) = parser.parse_args()

#initialize values from command line
host = options.host
port = int(options.port)
size = int(options.size)
hashtag = options.hashtag
print("[Checkpoint] Listening for Tweets that contain: " + hashtag)
hashtag = hashtag.strip()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((host,port))
#s.send(b'Hello, world')
#data = s.recv(size)
#s.close()
#print ('Received:', data)

#set consumer token + access token
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


#generate fernet key


api = tweepy.API(auth)
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        messages = status.text
        user = status.user.name
        key = Fernet.generate_key()
        print("[Checkpoint] New Tweet: " + messages + " | User: " + user)
        filteredMessage = messages.replace(hashtag, '')    #Gets rid of hashtag in the message
        f = Fernet(key)
        token = f.encrypt(filteredMessage.encode('utf-8'))  #ciphered text
        print("[Checkpoint] Encrypt: Generated Key: %s" % key)
        print("| Ciphertext: %s" % token)
        m = hashlib.md5()
        m.update(token)
        checksum = m.hexdigest()
        print("[Checkpoint] Generated MD5 Checksum: " + checksum)
        pickleCheckSum = pickle.dumps((key, token, checksum))
        print("[Checkpoint] Connecting to %s on port %s" % (host, port))
        s.connect((host,port))
        s.send(pickleCheckSum)  #bytes
        data = s.recv(size)

        print("[Checkpoint] Sending data %s" % pickleCheckSum)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=[hashtag])

