#  coding: utf-8 
import SocketServer
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Chris Lin
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

#check if our request is GET type
    #http_request -> ['GET', '/', 'HTTP/1.1']
    def checkget(self,http_request):
        if len(http_request)==3 and http_request[0]=='GET':          
	    return True
	else:
	    return False

    #handle status code
    def code_200(self,file_type,path):
        self.response =("HTTP/1.1 200 OK \nContent-Type: "+file_type+"\n\n"+open(path).read())

    def error_404(self,response):
        self.response += ("HTTP/1.1 404 Not Found\r\n"
                          "Connection: close\r\n"
                          "Content-Type: text/plain\n\n")
        
    def error_501(self,response):
        self.response += ("HTTP/1.1 501 Not Implemented\n"+
                        "Content-Type text/html\n\n")
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
	
        header = self.data.splitlines()[0]   #should return similar to "GET / HTTP/1.1" 
        http_request = header.split()        #should return something like ['GET', '/', 'HTTP/1.1']
	
	
	#call check_get function and find its absolute path
        if self.checkget(http_request)== True:
            getdata = http_request[1]
            path = os.path.abspath("www"+getdata)
            
	    #check if the path is a file
            if (os.path.isfile(path)) == True:
		file_type = path.split('.')[-1]
		if (file_type =='css'):
		    
		    file_type ="text/css"
		    self.code_200(file_type,path)

                elif (file_type=='html'):
                    file_type ="text/html"
		    self.code_200(file_type,path)
		else:
		    self.error_404(self.response)
	    #chekc if the path is a directory and open up html if exist
	    elif(os.path.isdir(path)) == True:
		path += "/index.html"
		if (os.path.isfile(path)):
			file_type = "text/html\n\n"
			self.code_200(file_type,path)
            else:
                self.error_404(self.response)
	else:
	    self.error_501(self.response)
      
        self.request.sendall(self.response)

   


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
