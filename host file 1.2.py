import socket
import time
class server_chat():
    def __init__(self):        
        self.host = '130.71.242.119'
        self.port = 5000
        self.clients = []
    def main(self):
        

        s = socket.socket(socket.AF_INET, socket. SOCK_DGRAM)
        s.bind((self.host, self.port))
        s.setblocking(0)

        quitting = False
        print("Server Started.")

        while not quitting:
            try:
                data, addr = s.recvfrom(1024)
                if "Quit" in str(data):
                    quitting = True
                if addr not in self.clients:
                    self.clients.append(addr)

                print (time.ctime(time.time()) + str(addr) + ": :" + str(data))
                for client in self.clients:
                    s.sendto(data, client)
            except:
                pass
        s. close()
server_chat.main(server_chat())
