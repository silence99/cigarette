import utils.LogMgr as log
import asyncio

class MessageCenter(object):
    def __init__(self):
        super().__init__()
        self._logger = log.GetLogger(self)
        self._logger.info("initialize configuration dispatching center ...")
        self._channels = {}  #client channels(stream protocal): record pairs
    
    def Register(self, channel):  #channel will be a client connection who need to be notified        
        key = "%s:%s" % (channel.ip, channel.port)
        self._logger.info("new connection is registering to center: %s" % key )
        self._channels[key] = channel

    def SendNotification(self, config):
            if len(self._channels) == 0:
                return
            for channel in self._channels:
                self._channels[channel].SendNotification(config)
            self._logger.debug("complete...")

MessageCenter = MessageCenter()
