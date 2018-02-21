# fourty_two

This is a simple client - server model that uses TCP socket connection in python.

The client can subscribe to a certain hashtag of the Tweets, and it filters out the message, encrypts the message, and sends it to the server.
The server receives the message, verifies the checksum, and uses the WolframAlpha API to get the answer to the question from the twitter.
If the message is not a valid question, it shuts down. The server side then speaks the question out loud, and sends the answer back to the 
client. The client verifies the checksum, and speaks the answer out loud.
