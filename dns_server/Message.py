import struct
from DNSQuery import DNSQuery
from DNSRecord import DNSRecord

class Message:
    @staticmethod
    def parse_message(bytes):
        msg = Message()
        (msg.id, msg.flags, msg.questions_RR, msg.answers_RR, msg.authority_RR, msg.additonal_RR) = struct.unpack_from('!HHHHHH', bytes, 0)
        msg.questions = []
        msg.answers = {}
        msg.authority = {}
        offset = 12
        for i in range(msg.questions_RR):
            query, offset = DNSQuery.parse_query(bytes, offset)
            msg.questions.append(query)
        for i in range(msg.answers_RR + msg.authority_RR + msg.additonal_RR):
            query, offset = DNSQuery.parse_query(bytes, offset)
            record, offset = DNSRecord.parse_record(bytes, offset, query.q_type == 2)
            msg.answers[query] = record
        return msg

    def to_bytes(self):
        bytes = struct.pack('!HHHHHH', self.id, self.flags, self.questions_RR, self.answers_RR, self.authority_RR, self.additonal_RR)
        for question in self.questions:
            bytes += question.to_bytes()
        for question, answer in self.answers.items() | self.authority.items():
            bytes += question.to_bytes()
            bytes += answer.to_bytes()
        return bytes