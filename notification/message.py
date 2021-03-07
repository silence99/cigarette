from .status import Status

CR = '\r'
CL = '\n'
NewLine = CR + CL
MessageFlags = 'CITI'
Version = '1.0'
MessageType = 'CONFIG'
ContentLength = 'content length'
ContentType = 'content type'
DefaultEncoding = 'utf-8'
Encoding = "encoding"   

class Message(object):
    
    def __init__(self):
        pass

    @classmethod
    def Generate(cls, content, headers=None, messageType=MessageType, contentType='text', encoding=DefaultEncoding):
        '''
        headers encoding with ascii, boday encoding with params
        '''
        head = []
        first = "%s %s %s" % (MessageFlags, Version, messageType)
        head.append(first)

        encodingExp = "%s: %s" % (Encoding, encoding)
        head.append(encodingExp)

        contentTypeExp = "%s: %s" % (ContentType, contentType)
        head.append(contentTypeExp)

        body = None if content is None else content.encode(encoding)
        length = 0 if body is None else len(body)
        contentLengthExp = "%s: %s" % (ContentLength, length)
        head.append(contentLengthExp)

        headExp = ""
        for h in head:
            headExp = "%s%s%s" % (headExp, h, NewLine)
        
        headExp += NewLine
        msg = headExp.encode('ascii') + body
        return msg


class ResponseMessage:
    def __init__(self):
        super().__init__()
        self.status = Status.UNKNOW
        self.content = ''
        self.version = '1.0'
        self.head = None    #bytes - split by \r\n\r\n
        self.body = None
        self.bodyObj = None
        self.contentType = 'text'
        self.encoding = 'utf-8'

    @classmethod    
    def GetMessage(cls, response):
        msg = ResponseMessage()
        # only read first line to check status currently
        msg.loadFromBuffer(response)

        return msg

    @classmethod
    def _getStatus(cls, st):
        for i in list(Status):
            if i.name == st:
                return i

        return Status.UNKNOW

    def loadFromBuffer(self, buffer):
        self._split(buffer)
        self.loadHead()
        self.loadBody()
    
    def _split(self, bytesContent):
        if bytesContent is not None:
            sp = bytesContent.split(("%s%s" % (NewLine, NewLine)).encode('ascii'))
            self.head = sp[0]
            self.body = sp[1]

    def loadHead(self):
        if self.head:
            sp = self.head.split(NewLine.encode('ascii'))
            statusExp = sp[0]
            sts = statusExp.split()
            if sts[0] == MessageFlags and sts[1] == Version:
                msg.version = Version
                msg.status = _getStatus(sts[2].upper())
            else:
                return None
            for line in sp[1:]:
                kvs = line.split(':')
                if len(kvs) == 2:
                    self.assignHead(kvs[0], kvs[1])

    def assignHead(self, key, v):
        if key == Encoding:
            self.encoding = v
        elif key == ContentType:
            self.contentType = v
        else:
            pass

    def loadBody(self):
        self.bodyObj = self.body.decode(encoding=self.encoding)

    