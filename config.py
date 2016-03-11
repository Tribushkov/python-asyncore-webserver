import rfc822
import time

HOST = 'localhost'
PORT = 80

ROOT_DIR = 'static'
CPU_COUNT = 1

HTTP_VERSION = '1.1'
SERVER_NAME = 'My custom http server'

date = rfc822.formatdate(time.time())

RESPONSE_403 = "HTTP/" + HTTP_VERSION + " 403 Forbidden\r\n"
RESPONSE_403 += "Server: " + SERVER_NAME + "\r\n"
RESPONSE_403 += "Date: " + str(date) + "\r\n"
RESPONSE_403 += "Content-Type: text/html; charset=UTF-8\r\n"
RESPONSE_403 += "Connection: close\r\n\r\n"
RESPONSE_403 += "<html><head><title>403 Forbidden</title></head><body><h1>403 Forbidden</h1></body></html>"

RESPONSE_404 = "HTTP/" + HTTP_VERSION + " 404 Not Found\r\n"
RESPONSE_404 += "Server: " + SERVER_NAME + "\r\n"
RESPONSE_404 += "Date: " + str(date) + "\r\n"
RESPONSE_404 += "Content-Type: text/html; charset=UTF-8\r\n"
RESPONSE_404 += "Connection: close\r\n\r\n"
RESPONSE_404 += "<html><head><title>404 Not found</title></head><body><h2>404 Not found</h2></body></html>"

RESPONSE_405 = "HTTP/" + HTTP_VERSION + " 405 Method Not Allowed\r\n"
RESPONSE_405 += "Server: " + SERVER_NAME + "\r\n"
RESPONSE_405 += "Date: " + str(date) + "\r\n"
RESPONSE_405 += "Content-Type: text/html; charset=UTF-8\r\n"
RESPONSE_405 += "Connection: close\r\n\r\n"
RESPONSE_405 += "<html><head><title>405</title></head><body><h2>405 Method Not Allowed</h2></body></html>"
