import socket
import time
import pickle
from Message import Message


class Server:

    def __init__(self, port, another_server, cache_file):
        self.port = port
        self.forwarder = another_server
        self.cache_file = cache_file
        with open(self.cache_file, 'rb') as f:
            self.cache = pickle.load(f)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('127.0.0.1', self.port))
            print(f"Start server on 127.0.0.1 port {self.port}...")
            while True:
                try:
                    data, address = s.recvfrom(1024)
                    s.sendto(self.generate_answer(data), address)
                except socket.timeout:
                    continue
                except Exception as e:
                    print(e)
                    continue

    def generate_answer(self, bytes):
        msg = Message.parse_message(bytes)
        for question in msg.questions:
            if not question in self.cache or self.cache[question].exp_time < int(time.time()):
                return self.ask_another_server(bytes)
            if question.q_type == 6:
                msg.authority[question] = self.cache[question]
                msg.authority_RR += 1
            else:
                msg.answers[question] = self.cache[question]
                msg.answers_RR += 1
            print('Get from cache.txt')
        msg.flags = 0x8580
        return msg.to_bytes()

    def ask_another_server(self, bytes):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(self.forwarder)
            s.send(bytes)
            data = s.recv(1024)
            self.cache.update(Message.parse_message(data).answers)
            return data

    def save_cache(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)


