import time
from .status import Status


class Record(object):
    def __init__(self, uid, user=None, ip=None, port=None, startSend=None, endSend=None, lenSend=-1, lenRecv=-1):
        self.id = uid
        self.user = user
        self.ip = port
        self.port = port
        self.startSend = startSend if startSend is not None else time.time()
        self.endSend = endSend
        self.lenSend = lenSend
        
        self.startRecv = None
        self.endRecv = None
        self.lenRecv = lenRecv

        self.status = Status.UNKNOW

class History(object):
    def __init__(self):
        self.summary = {}   #key: ip:port, record[]
    
    def AddRecord(self, ip, port, record):
        key = '%s:%s' % (ip, port)

        if key in self.summary:
            self.summary[key].append(record)
        
        else:
            self.summary[key] = [record]

    def Clear(self):
        self.summary.clear()
        
Summary = History()
