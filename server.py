#server side / host
import configparser
import base64
import sys, socket, select
from Crypto.Cipher import AES
import hashlib
import os
import signal

os.system("clear")
print("""

	 ____  ____  ____   __   _  _      __  ____   ___ 
	(    \(  _ \(  __) / _\ ( \/ ) ___(  )(  _ \ / __)
	 ) D ( )   / ) _) /    \/ \/ \(___))(  )   /( (__ 
	(____/(__\_)(____)\_/\_/\_)(_/    (__)(__\_) \___)


		    Secure IRC by DreamSec
		       dreambooter.xyz

""")

def sigint_handler(signum, frame):
    print('\n[error] user interupt')
    print("[info] shutting down DREAM-IRC \n\n")
    sys.exit()	

signal.signal(signal.SIGINT, sigint_handler)

def hasher(key):
	hash_object = hashlib.sha512(key)
	hexd = hash_object.hexdigest()
	hash_object = hashlib.md5(hexd)
	hex_dig = hash_object.hexdigest()
	return hex_dig	

def encrypt(secret,data):
	BLOCK_SIZE = 32
	PADDING = '{'
	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
	EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
	cipher = AES.new(secret)
	encoded = EncodeAES(cipher, data)
	return encoded

def decrypt(secret,data):
	BLOCK_SIZE = 32
	PADDING = '{'
	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
	DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
	cipher = AES.new(secret)
	decoded = DecodeAES(cipher, data)
	return decoded

config = configparser.RawConfigParser()   
config.read(r'dream.conf')

HOST = config.get('config', 'HOST')
PORT = int(config.get('config', 'PORT'))
PASSWORD = config.get('config', 'PASSWORD')
VIEW = str(config.get('config', 'VIEW'))
key = hasher(PASSWORD)
SOCKET_LIST = []
RECV_BUFFER = 4096


def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    SOCKET_LIST.append(server_socket)

    print("[Server] Started on port " + str(PORT))

    while 1:

        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

        for sock in ready_to_read:

            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print("[Server] User [(%s, %s)] connected" % addr)
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    data = decrypt(key,data)
                    if data:

                        broadcast(server_socket, sock,encrypt(key,"\r" + data))
                        if VIEW == '1':
                          print(data)
                    else:

                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        broadcast(server_socket, sock,encrypt(key,"[Server] [(%s, %s)] Has left the server.\n" % addr))

                except:
                    broadcast(server_socket, sock, "[Server] User [(%s, %s)] is offline\n" % addr)
                    continue

    server_socket.close()

def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:

        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :

                socket.close()

                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

if __name__ == "__main__":

    sys.exit(chat_server())
