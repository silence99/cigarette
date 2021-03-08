
import asyncio
import uuid
import time
import json
from .center import MessageCenter
from .record import Record, Summary
import utils.LogMgr as log
from .message import Message, ResponseMessage
from .status import Status


class Agent(asyncio.Protocol):

    def __init__(self, options=None):
        super().__init__()
        self.logger = log.GetLogger(self)
        self.ip = None
        self.port = None
        self.staged = {}  # key: uuid, value: record
        self.options = options
        if isinstance(options, dict):
            self.encoding = 'utf-8' if 'encoding' not in options else options['encoding']
        else:
            self.encoding = 'utf-8'

    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        self.ip = peername[0]
        self.port = peername[1]
        self.logger.debug('Connection from {}'.format(peername))
        self.logger.debug('register messages center')
        self.RegisterToCenter()

    def data_received(self, data):
        pass

    """ def data_received(self, data):
        try:
            self.logger.debug("get %s bytes messages" % len(data))
            t = time.time()
            response = ResponseMessage.GetMessage(data)
            content = response.bodyObj
            uid = content.split(':')[0]
            if uid not in self.staged:
                self.logger.warn("received unrecord notification")
                record = Record(uid, ip=self.ip,
                                port=self.port, lenRecv=len(data))
                record.startRecv = time.time()
                record.status = Status.FAILD
            else:
                record = self.staged.pop(uid)
                record.startRecv = t
                record.status = Status.OK
                record.lenRecv = len(data)
            Summary.AddRecord(record.ip, record.port, record)
        except Exception as e:
            self.logger.error("received invalid message: %s" %
                              data.decode('utf-8')) """

    def connection_lost(self, exc):
        self.logger.info('%s:%s connection is closed.')
        if len(self.staged) == 0:
            return

        self.logger.warn(
            "not all notification completed when connection close")
        for uid in self.staged:
            record = self.staged[uid]
            t = time.time()
            record.startRecv = t
            record.status = Status.UNCOMPLETED
            Summary.AddRecord(record)

        self.staged.clear()

    def RegisterToCenter(self):
        MessageCenter.Register(self)

    def SendNotification(self, data):
        if data is None:
            self.logger.warn(
                "the configuration notification contains none message")
            return

        self.logger.debug(
            "sync configuration changing message to %s:%s" % (self.ip, self.port))
        self.transport.write(data)

    def SyncToClient(self, config):
        if config is None:
            self.logger.warn(
                "the configuration notification contains none message")
            return

        uid = str(uuid.uuid4())

        msg = {
            "session": uid,
            "config": config
        }
        msg = json.dumps(msg)
        msgSend = Message.Generate(msg)

        record = Record(uid, ip=self.ip, port=self.port,
                        startSend=time.time(), lenSend=len(msgSend))
        self.staged[uid] = record

        self.transport.write(msgSend)
        record.endSend = time.time()
