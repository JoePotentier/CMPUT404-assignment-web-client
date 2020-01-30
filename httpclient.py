#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re

# you may use urllib to encode data appropriately
import urllib.parse as parser


def help():
    print("httpclient.py [GET/POST] [URL]\n")


class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

    def __str__(self):
        return self.body


class HTTPClient(object):
    # def get_host_port(self,url):

    def connect(self, host, port):
        if port == None:
            port = 80
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        res_line = data.splitlines()[0]
        return res_line.split(" ")[1]

    def get_headers(self, data):
        lines = data.splitlines()
        i = 0
        while lines[i] != "":
            i += 1
        i += 1
        headers = lines[:-i]
        return "\r\n".join(headers)

    def get_body(self, data):
        lines = data.splitlines()
        i = 0
        while lines[i] != "":
            i += 1
        i += 1
        body = lines[i:]
        return "".join(body)

    def sendall(self, data):
        # print(data)
        self.socket.sendall(data.encode("utf-8"))

    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if part:
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode("utf-8")

    def GET(self, url, args=None):
        code = 500
        body = ""
        self.parseURL(url)
        # print(self.url)
        self.connect(self.url.netloc, self.url.port)
        toSend = f"GET {self.url.path} HTTP/1.1\r\n"
        toSend += f"Host: {self.url.netloc}\r\n"
        toSend += "User-Agent: curl/7.65.3\r\n"
        toSend += "Accept: */*\r\n"
        toSend += "Connection: close\r\n"
        toSend += "\r\n"
        self.sendall(toSend)
        response = self.recvall(self.socket)
        code = self.get_code(response)
        body = self.get_body(response)
        print(self.get_headers(response))
        self.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):

        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if command == "POST":
            return self.POST(url, args)
        else:
            return self.GET(url, args)

    def parseURL(self, url):
        self.url = parser.urlparse(url)


if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if len(sys.argv) <= 1:
        help()
        sys.exit(1)
    elif len(sys.argv) == 3:
        print(client.command(sys.argv[2], sys.argv[1]))
    else:
        print(client.command(sys.argv[1]))
