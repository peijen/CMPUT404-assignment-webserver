#  coding: utf-8 
import SocketServer
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


class MyWebServer(SocketServer.BaseRequestHandler):



    #initialize response
    response=""
#first define all the functions we need first

    #check if our request is GET type
    #http_request -> ['GET', '/', 'HTTP/1.1']
    def check_get(self,http_request):
        if http_request==3:          
            if http_request[0]=='GET':
                return True
            else:
                return False
            
    #check the path of file and directory
    def check_file(self,path):
        if (os.path.isfile(path)) and (os.path.isdir(path)):
            return True
        else:
            return False


    #handle status code
    def code_200(file_type,path):
        self.response =("HTTP/1.1 200 OK \n File Type: "+file_type+"\n\n"+open(path).read())

    def error_404(self,response):
        self.response = ("HTTP/1.1 404 Not Found\n")
        
    def error_501(self,response):
        self.response = ("HTTP/1.1 501 Not Implemented\n")
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        header = self.data.splitlines()[0]   #should return similar to "GET / HTTP/1.1" 
        http_request = header.split()        #should return something like ['GET', '/', 'HTTP/1.1']


        print(header.split())
        print('\n')
        print(self.data)
        self.request.sendall("OK")


 


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
