from Server import Server
from DNSQuery import DNSQuery
from DNSRecord import DNSRecord

if __name__ == '__main__':
    server = Server(53, ('8.8.8.8', 53), 'cache.txt')
    try:
        server.start()
    except KeyboardInterrupt:
        server.save_cache()