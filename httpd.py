import socket
import mimetypes
import os
import urllib
import asyncore
import sys, getopt
from config import *


class HTTPHandler(asyncore.dispatcher):
    def __init__(self, client, path):
        self.path = path
        asyncore.dispatcher.__init__(self, client)
        self.data_to_write = []

    def handle_read(self):
        request_header = self.recv(4096)
        request_header = urllib.unquote(request_header)

        date = rfc822.formatdate(time.time())

        method = request_header[:3]

        if '?' in request_header:
            request_header = request_header.split('?')[0]
            file_path = ROOT_DIR + '/' + request_header[5:]
        else:
            request_type = ''
            if request_header[0].lower() == 'g':
                request_type = 'GET /'
            if request_header[0].lower() == 'h':
                request_type = 'HEAD /'
            if request_header[0].lower() == 'p':
                request_type = 'POST /'
            file_path = ROOT_DIR + '/' + request_header[len(request_type):request_header.find('\n')-len(' HTTP/1.1 ')]

        if method == 'POS':
            self.send(RESPONSE_405)
            self.close()
            return

        if os.path.isdir(file_path) or not file_path:
            file_path += 'index.html'
            if not os.path.isfile(file_path):
                self.send(RESPONSE_403)
                self.close()
                return
        if os.path.isfile(file_path):
            file_text = open(file_path, 'r').read()
        else:
            self.send(RESPONSE_404)
            self.close()
            return

        file_size = os.path.getsize(file_path)
        file_type = mimetypes.guess_type(file_path, strict=True)[0]

        if self.validate_path(file_path):
            self.send(RESPONSE_403)
            self.close()
            return
        else:
            response = ''
            response += "HTTP/" + HTTP_VERSION + " 200 OK\r\n"
            response += "Server: " + SERVER_NAME + "\r\n"
            response += "Date: " + str(date) + "\r\n"
            response += "Content-Type: " + str(file_type) + "\r\n"
            response += "Content-Length: " + str(file_size) + "\r\n"
            response += "Connection: close\r\n\r\n"
            if method == 'HEA':
                self.send(response)
                self.close()
            else:
                response += file_text

        self.data_to_write.append(response)

    def writable(self):
        response = bool(self.data_to_write)
        return response

    def handle_write(self):
        data = self.data_to_write.pop()

        sent = self.send(data[:4096])
        if sent < len(data):
            remaining = data[sent:]
            self.data_to_write.append(remaining)

        if not self.writable():
            self.handle_close()

    def validate_path(self, file_path):
        level = 1
        chunks = file_path.split('/')
        for chunk in chunks:
            if chunk == "..":
                level -= 1
            else:
                level += 1
            if level < 1:
                return True
        return False


class HTTPServer(asyncore.dispatcher):
    def __init__(self, addr):
        self.addr = addr

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        self.set_reuse_addr()
        self.bind(self.addr)
        self.listen(500)
        print 'Listening on port %d' % addr[1]

    def handle_accept(self):
        try:
            client, addr = self.accept()
            HTTPHandler(client, addr)
        except:
            return

if __name__ == '__main__':
    myopts, args = getopt.getopt(sys.argv[1:], "r:c:")
    for o, a in myopts:
        if o == '-r':
            ROOT_DIR = a
        elif o == '-c':
            CPU_COUNT = int(a)

    server = HTTPServer((HOST, PORT))
    for i in range(1, CPU_COUNT):
        os.fork()
    asyncore.loop(timeout=0.1)
