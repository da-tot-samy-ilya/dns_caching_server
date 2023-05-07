from Utils import Utils
import struct

class DNSQuery:

    @staticmethod
    def parse_query(bytes, offset):
        query = DNSQuery()
        query.url, offset = Utils.parse_url(bytes, offset)
        query.q_type, offset = Utils.parse_short(bytes, offset)
        query.q_class, offset = Utils.parse_short(bytes, offset)
        return query, offset

    def to_bytes(self):
        return Utils.url_to_bytes(self.url) + struct.pack('!HH', self.q_type, self.q_class)

    def __hash__(self):
        return hash(self.url) ** hash(self.q_type) ** hash(self.q_class)

    def __eq__(x, y):
        return x.url == y.url and x.q_type == y.q_type and x.q_class == y.q_class