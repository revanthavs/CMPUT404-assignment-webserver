#  coding: utf-8 
import socketserver
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

debug = 1

class MyWebServer(socketserver.BaseRequestHandler):

    # Assumes the request is GET
    def get_requested_path(self, request_data):
        curr_index = 6
        requested_path = ""

        while request_data[curr_index] != " ":
            requested_path += request_data[curr_index]
            curr_index += 1

        return requested_path

    def check_requested_path(self, allowed_directory, requested_path):
        if os.path.commonprefix([os.path.abspath(allowed_directory), os.path.abspath(requested_path)]) == os.path.abspath(allowed_directory):
            # The path is a subpath of www directory
            return True
        else:
            # The path is not a subpath of www directory which is not safe
            return False            

    # Allows only files in directory www/
    def handle(self):
        self.data = self.request.recv(1024).strip()
        data = str(self.data)

        if data[2] == 'G' and data[3] == 'E' and data[4] == 'T':
            allowed_directory = "www/"
            requested_path = allowed_directory + self.get_requested_path(data)

            try:
                if os.path.isdir(os.path.abspath(requested_path)) and self.check_requested_path(allowed_directory, requested_path):
                    if requested_path[-1] != '/':
                        self.request.sendall(bytearray("HTTP/1.1 301 MOVED PERMANENTLY\r\nLocation: http://127.0.0.1:8080"+self.get_requested_path(data)+"/\r\n\r\n", 'utf-8'))
                        return
                    else:
                        requested_path += "index.html"

                        with open(requested_path, "r") as f:
                            self.request.send(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/"+requested_path.split(".")[-1]+"\r\n\r\n",'utf-8'))
                            self.request.sendall(bytearray(f.read(),'utf-8'))

                elif os.path.isfile(requested_path) and self.check_requested_path(allowed_directory, requested_path):
                    with open(requested_path, "r") as f:
                        self.request.send(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/"+requested_path.split(".")[-1]+"\r\n\r\n",'utf-8'))
                        self.request.sendall(bytearray(f.read(),'utf-8'))
                else:
                    self.request.sendall(bytearray("HTTP/1.1 404 NOT FOUND\r\n\r\n",'utf-8'))
            except FileNotFoundError:
                self.request.send(bytearray("HTTP/1.1 404 NOT FOUND\r\n\r\n",'utf-8'))
        else:
            self.request.send(bytearray("HTTP/1.1 405 METHOD NOT ALLOWED\r\n\r\n",'utf-8'))

        # self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True

    # Create the server, binding to localhost on port 8080 using with
    with socketserver.TCPServer((HOST, PORT), MyWebServer) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

    # # Create the server, binding to localhost on port 8080
    # server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # # Activate the server; this will keep running until you
    # # interrupt the program with Ctrl-C
    # server.serve_forever()
