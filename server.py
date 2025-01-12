#  coding: utf-8 
import re
import socketserver
from urllib import response

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


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        # Get path and split it into filename
        self.data = self.data.decode("utf-8")
        headers = self.data.split('\r\n')
        filename = headers[0].split()[1]

        # If index 0 of header is not GET reponse with 405
        if headers[0].split()[0] != 'GET':
            response = f'HTTP/1.1 405 Not ALLOWED\r\nContent-Type: text/html\r\n'
        else:
            # Add index.html to any path that ends with /
            if filename[-1] == '/':
                filename += 'index.html'
            try:
                # If path name ends with css, open & read content of file and respond    
                if filename[-3:] == 'css':
                    url = 'www' + filename
                    file = open(url)
                    content = file.read()
                    file.close()
                    response = f'HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nContent-Length: {len(content)}\r\n\r\n{content}'
                # If path starts with /.. respond with 404
                elif filename[:3] == '/..':
                    response = f'HTTP/1.1 404 Not FOUND\r\nContent-Type: text/html\r\n'
                # If path ends with html, open & read content of file respond 
                elif filename[-4:] == 'html':
                    url = 'www' + filename
                    file = open(url)
                    content = file.read()
                    file.close()
                    response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\n\r\n{content}'
                # If path is none of the above, respond with 301  
                else:
                    url = filename + '/'
                    response =f'HTTP/1.1 301 Moved Permanently\r\nLocation: {url}\r\n'
            except FileNotFoundError:
                response = f'HTTP/1.1 404 Not FOUND\r\nContent-Type: text/html\r\n'    
        self.request.sendall(bytearray(response,'utf-8'))        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

