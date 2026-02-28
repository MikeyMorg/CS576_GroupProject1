# Group Programming Assignment #1
# Group Members: Michael Morgan, Maximus Daversa, Paris Cabatit, Justin Cruz
# Instructor: Dr. Wei Wang
# 
#

# Import Statements
import socket

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
        return None
    
    # Create an array for the encoded message
    encoded_msg = []

    # For loop to ensure message only contains the printable ASCII characters and wraps in the event it overflows
    for i in msg:
        encode = ord(i)

        # Ensure only printable ASCII messages are in the inputted message
        if encode < 32 or encode > 126:
            print("Message contains invalid ASCII characters that cannot be printed.")
            return None
        
        # Wrap if we're at the last printable ASCII character '~', to ' '. (Space)
        if encode == 126: 
            encoded_msg.append(chr(32))
        elif encode == 90:
            encoded_msg.append(chr(65))
        elif encode == 122:
            encoded_msg.append(chr(97))
        else:
            encoded_msg.append(chr(encode + 1))

    return ''.join(encoded_msg)

def client_handle(conn, addr):
    #Say where we got our connection from
    print("Connection from " + addr[0] + ":" + str(addr[1]))

    #Set connection timeout length
    conn.settimeout(10)

    # Create a buffer
    buffer = b""

    #While loop to read in buffer until new line is entered
    while b"\n" not in buffer:
        chunk = conn.recv(MAX_SIZE)
        
    # If recv returns empty bytes, the client disconnected
        if not chunk:
            print("Client disconnected.")
            conn.close()
            return None

        # Add the chunk to the buffer
        buffer = buffer + chunk

        # Reject if max_size is exceeded. +1 for the newline character.
        if len(buffer) > MAX_SIZE + 1:
            print("Message is too large")
            conn.close()
            return None

    # Decode the new line and strip the newline
    message = buffer.decode('utf-8').rstrip("\r\n")
    
    #Print inputted message
    print("Received message: " + message)

    #encode the message
    encoded_message = encode_message(message)

    # Ensure message encoding was successful
    if encoded_message is None:
        conn.sendall("Message encoding failed.\n".encode('utf-8'))
        conn.close()
        return None
    else:
        conn.sendall((encoded_message + "\n").encode('utf-8'))

    conn.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', PORT))
    server_socket.listen(10)
    print("Server listening for a connection at current port " + str(PORT))

    while True:
        conn, addr = server_socket.accept()
        client_handle(conn,addr)

main()