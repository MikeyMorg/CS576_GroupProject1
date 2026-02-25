# Group Programming Assignment #1
# Group Members: Michael Morgan, Maximus Daversa, Paris Cabatit, Justin Cruz
# Instructor: Dr. Wei Wang
# 
#

# Import Statements
import socket
# import argparse //Not sure if this will be needed, may make it easier

# Set constants
PORT = 3490
MAX_SIZE = 256

# Encode message by increase each charcter in a phrase by one place in ASCII
def encode_message(msg: str) -> str:
    # Get rid of newline
    msg = msg.rstrip("\r\n")

    # Force incoming message to be limited to the maximum size
    if len(msg) > MAX_SIZE:
        print("Message exceeds max length of 256 characters.")
        return 0
    
    # Create an array for the encoded message
    encoded_msg = []

    # For loop to ensure message only contains the printable ASCII characters and wraps in the event it overflows
    for i in msg:
        encode = ord(i)

        # Ensure only printable ASCII messages are in the inputted message
        if encode < 32 or encode > 126:
            print("Message contains invalid ASCII characters that cannot be printed.")
        
        # Wrap if we're at the last printable ASCII character '~', to ' '. (Space)
        if encode == 126: 
            encoded_msg.append(chr(32))
        else:
            encoded_msg.append(chr(encode + 1))

    return ''.join(encoded_msg)

