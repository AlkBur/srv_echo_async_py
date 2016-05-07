import asyncore
import socket

# Server - асинхронный echo сервер
class Server(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(10)

    def handle_accept(self):
        # when we get a client connection start a dispatcher for that
        # client
        pair = self.accept()
        if pair is not None:
            socket, address = pair
            print 'Connection by', address
            EchoHandler(socket)

# EchoHandler - Обработка полученных данных
class EchoHandler(asyncore.dispatcher_with_send):
    # dispatcher_with_send extends the basic dispatcher to have an output
    # buffer that it writes whenever there's content
    def handle_read(self):
        data = self.recv(1024)
        print 'received = ', data
        if data:
            if data == "Close" or data == "close":
                self.close()
            else:
                self.send(data)

s = Server('0.0.0.0', 2222)
asyncore.loop()
