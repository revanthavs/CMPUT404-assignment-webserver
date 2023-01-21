#  coding: utf-8 
import socketserver

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

debug = 0

Allowed_paths = {"/":"www/index.html", "/index.html":"www/index.html", "/base.css":"www/base.css"}

class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        data = str(self.data)

        if data[2] == 'G' and data[3] == 'E' and data[4] == 'T':
            curr_index = 6
            requested_path = ""

            while data[curr_index] != " ":
                requested_path += data[curr_index]
                curr_index += 1

            if requested_path in Allowed_paths:

                if Allowed_paths[requested_path] == "www/index.html":
                    self.request.send(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/html;",'utf-8'))
                else:
                    self.request.send(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/css;",'utf-8'))

                # self.request.send(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/html;",'utf-8'))

                with open(Allowed_paths[requested_path], "r") as f:
                    curr_lines = f.readlines()
                    if debug == 1:
                        print(curr_lines)
                    
                    for curr_line in curr_lines:
                        self.request.sendall(bytearray(curr_line,'utf-8'))

                if debug == 1:
                    print("Reqested_path: ", requested_path)
                    print("In Allowed_paths: ", Allowed_paths[requested_path])
                    # print(reqested_path[2], reqested_path[3], reqested_path[4])
                    # print(type(self.data))
                    print ("Got a request of: %s\n" % self.data)
            else:
                self.request.send(bytearray("HTTP/1.1 404 NOT FOUND\r\n;",'utf-8'))                

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
