Programming Assignment #1
CS 576 - Computer Networks and Distributed Systems
Instructor: Dr. Wei Wang

Group Members:
Michael Morgan
Maximus Daversa
Paris Cabatit
Justin Cruz

Overview:
Our project implements a TCP client-server application. The server we made will accept a connection from a client, be able to receive a text message that has a maximum of 256 characters, and encode the message by shifting all the characters forward by one position based on the ASCII table, and finally returning the encoded message to the client.

System Design:
-Architecture:
-Encoding Logic:

Implementation:
-Server:
-Client:

How to Run:
1. Open a terminal in the project directory and run the following command 'python server.py'
Expected Output: "Server listening for a connection at current port 3490"
2. Open a second terminal window and navigate to same projcet directory
3. Run the client 'python client.py'
4. Enter a message when promopted
5. To exit client, type 'QUIT' or press 'Ctrl + C'

Testing and Results:
1 Normal Run Screenshot

1 Error Handling Screenshot

Conclusion:
With this assignemtn we were able to fully implement a TCP client-server application utilziign Python socket programming. We have teh server waiting for client connections, listening to it, validating the inputs, and encoding the messages using ASCII shifting, and finally returning an encoded result. We were also able to have error handling for messages longer than 256 charcaters and the ensuring of only prinatable ASCII characters accepted. We have error handling methods on both the client and the server. From all of this, we have a working implementation of TCP communcation, with input validation and basic design.

Source Code:


