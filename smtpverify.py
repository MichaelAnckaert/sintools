#!/usr/bin/env python3
# smtpverify.py
# Verify usernames for the given SMTP server

import socket
import sys

def get_usernames(filename: str) -> list[str]:
    """Read the username file and return a list of cleaned usernames.

    We remove the \r and \n characters from each line.
    """
    try:
        with open(filename, 'r') as f:
            return [line.rstrip() for line in f.readlines()] 
    except FileNotFoundError:
        print(f"Could not find file '{filename}'!")
        sys.exit(1)


def validate_users(server_ip: str, usernames: list[str]):
    print(f"Connecting to {server_ip}...")
    # Create the connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection = s.connect((server_ip, 25))
    except Exception as e:
        print(f"Something went wrong connecting to {server_ip}: {e}")
        sys.exit(1)

    print("Connected established")

    # Receive the banner
    s.recv(1024)

    for username in usernames:
        command = f"VRFY {username}\r\n"
        s.send(command.encode())
        result = s.recv(1024).decode()

        if result.startswith('252 '):
            print(f"User '{username}' is accepted by the target system")

    s.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: smtpverify.py <server ip> <usernamefile>")
        sys.exit(0)

    server_ip = sys.argv[1]
    username_file = sys.argv[2]
    usernames = get_usernames(username_file)

    validate_users(server_ip, username_file)
