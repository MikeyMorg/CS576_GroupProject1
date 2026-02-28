# Group Programming Assignment #1
# Group Members: Michael Morgan, Maximus Daversa, Paris Cabatit, Justin Cruz
# Instructor: Dr. Wei Wang
# 
#

# Import statements
import socket
import sys

# Constants
SERVER_HOST = 'localhost'      # Server address (use '127.0.0.1' for local)
SERVER_PORT = 3490              # Must match server port
MAX_MESSAGE_SIZE = 256          # Maximum message length in characters
CONNECTION_TIMEOUT = 10         # Seconds to wait for server response
MAX_RETRY_ATTEMPTS = 3          # Number of times to retry on error

# User instructions
USER_INSTRUCTIONS = """
This client connects to an encoding server that transforms messages by
shifting each character to the next ASCII character.

Example: "Hello World" becomes "Ifmmp!Xpsme"

INSTRUCTIONS:
1. Ensure the server is running before starting this client
2. Enter your message when prompted
3. Message must be 256 characters or less
4. Only printable ASCII characters are allowed
5. Type 'QUIT' to exit the program
6. Type 'HELP' to see these instructions again

TROUBLESHOOTING:
- "Connection refused": Server is not running
- "Connection timed out": Server is busy or network issues
- "Invalid characters": Your message contains non-printable ASCII
"""

# Helper functions
def display_instructions():
    """Display user instructions to the console."""
    print(USER_INSTRUCTIONS)

def validate_message(message: str) -> tuple[bool, str]:
    """
    Validate that a message meets all requirements.
    
    Args:
        message: The message string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check for empty message
    if not message or message.isspace():
        return False, "Message cannot be empty."
    
    # Check length (server will also check, but we check early)
    if len(message) > MAX_MESSAGE_SIZE:
        return False, f"Message exceeds maximum length of {MAX_MESSAGE_SIZE} characters."
    
    # Check for newline characters (would break protocol)
    if '\n' in message:
        return False, "Message cannot contain newline characters."
    
    # Check for valid printable ASCII characters (matches server's validation)
    for i, char in enumerate(message):
        ascii_val = ord(char)
        if ascii_val < 32 or ascii_val > 126:
            return False, f"Invalid character at position {i+1}: '{char}' (ASCII {ascii_val}). Only printable ASCII characters (32-126) are allowed."
    
    return True, ""

def get_user_message() -> tuple[bool, str]:
    """
    Prompt user for a message and validate it.
    
    Returns:
        Tuple of (should_continue, message)
        should_continue: False if user wants to quit
        message: The validated message string
    """
    while True:
        try:
            user_input = input("\n📝 Enter message (or 'QUIT' to exit, 'HELP' for instructions): ").strip()
            
            # Check for special commands
            if user_input.upper() == 'QUIT':
                print("Goodbye")
                return False, ""
            
            if user_input.upper() == 'HELP':
                display_instructions()
                continue
            
            # Validate the message
            is_valid, error_msg = validate_message(user_input)
            
            if is_valid:
                return True, user_input
            else:
                print(f"Error: {error_msg}")
                print("Please try again.")
                
        except KeyboardInterrupt:
            print("\n\n Interrupted by user. Goodbye!")
            return False, ""
        except Exception as e:
            print(f"Unexpected error reading input: {e}")
            return False, ""

def communicate_with_server(message: str) -> tuple[bool, str]:
    """
    Connect to server, send message, and receive encoded response.
    
    Args:
        message: The message to encode
        
    Returns:
        Tuple of (success, result)
        success: True if operation succeeded
        result: Encoded message on success, error message on failure
    """
    # Create a new socket for each attempt
    client_socket = None
    
    try:
        # Create TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set timeout to prevent hanging
        client_socket.settimeout(CONNECTION_TIMEOUT)
        
        # Connect to server
        print(f"Connecting to server at {SERVER_HOST}:{SERVER_PORT}...")
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected successfully")
        
        # Send the message with newline terminator (as expected by server)
        print(f"📤 Sending message ({len(message)} characters)...")
        client_socket.sendall((message + "\n").encode('utf-8'))
        
        # Receive the encoded response
        # Server sends encoded message + newline
        response_buffer = b""
        
        # Read until we get a newline (server's message terminator)
        while b"\n" not in response_buffer:
            try:
                chunk = client_socket.recv(MAX_MESSAGE_SIZE + 1)  # +1 for newline
                
                # If recv returns empty bytes, server disconnected
                if not chunk:
                    return False, "Server closed connection unexpectedly."
                
                response_buffer += chunk
                
                # Prevent infinite loop if server sends too much data
                if len(response_buffer) > MAX_MESSAGE_SIZE + 10:  # Safety margin
                    return False, "Server response exceeded expected size."
                    
            except socket.timeout:
                return False, "Connection timed out while waiting for server response."
            except socket.error as e:
                return False, f"Socket error while receiving: {e}"
        
        # Decode and strip the newline
        encoded_message = response_buffer.decode('utf-8').rstrip("\r\n")
        
        return True, encoded_message
        
    except ConnectionRefusedError:
        return False, f"Connection refused. Is the server running at {SERVER_HOST}:{SERVER_PORT}?"
    except socket.timeout:
        return False, "Connection timed out. Server may be busy."
    except socket.gaierror:
        return False, f"Invalid hostname: {SERVER_HOST}"
    except Exception as e:
        return False, f"Unexpected error: {e}"
    finally:
        # Always close the socket
        if client_socket:
            client_socket.close()
            print("Connection closed.")

def main():
    """
    Main program loop.
    Handles user interaction and coordinates with server communication.
    """
    # Display welcome message and instructions
    print("\n" + "="*60)
    print("     MESSAGE ENCODING CLIENT - TCP IMPLEMENTATION")
    print("="*60)
    display_instructions()
    
    # Track statistics for the session
    stats = {
        "messages_sent": 0,
        "successful_encodings": 0,
        "failed_attempts": 0
    }
    
    # Main program loop
    while True:
        # Get message from user
        should_continue, message = get_user_message()
        
        if not should_continue:
            break
        
        stats["messages_sent"] += 1
        
        # Communicate with server (with retry logic)
        attempts = 0
        success = False
        
        while attempts < MAX_RETRY_ATTEMPTS and not success:
            attempts += 1
            
            if attempts > 1:
                print(f"Retry attempt {attempts}/{MAX_RETRY_ATTEMPTS}...")
            
            success, result = communicate_with_server(message)
            
            if success:
                # Display successful result
                print("\n" + "✓"*50)
                print("ENCODING SUCCESSFUL")
                print("✓"*50)
                print(f"Original: {message}")
                print(f"Encoded:  {result}")
                print("✓"*50 + "\n")
                stats["successful_encodings"] += 1
            else:
                # Display error message
                print(result)
                if attempts < MAX_RETRY_ATTEMPTS:
                    print(f"Retrying... ({attempts}/{MAX_RETRY_ATTEMPTS})")
                else:
                    print(f"Failed after {MAX_RETRY_ATTEMPTS} attempts.")
                    stats["failed_attempts"] += 1
        
        # Ask if user wants to continue (optional)
        if stats["messages_sent"] > 0 and stats["messages_sent"] % 3 == 0:
            try:
                choice = input("\n💬 Send another message? (y/n): ").strip().lower()
                if choice not in ['y', 'yes']:
                    print("Goodbye")
                    break
            except KeyboardInterrupt:
                print("\nGoodbye")
                break
    
    # Display session summary
    print("\n" + "="*60)
    print("SESSION SUMMARY")
    print("="*60)
    print(f"Messages attempted: {stats['messages_sent']}")
    print(f"Successful encodings: {stats['successful_encodings']}")
    print(f"Failed attempts: {stats['failed_attempts']}")
    print("="*60 + "\n")


# Program entry point
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program terminated by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
