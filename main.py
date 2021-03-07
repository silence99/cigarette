import asyncio
import utils.LogMgr as log
from notification.agent import Agent
from notification.center import MessageCenter

logger = log.GetLogger()

async def handle_queries(reader, writer):
    pass

async def start_server(addr='localhost', port=8080):
    loop = asyncio.get_running_loop()
    svr = await loop.create_server(lambda: Agent(), addr, port)
    host = svr.sockets[0].getsockname()  # 获得这个服务器的第一个套接字的地址和端口
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))  # 在控制台中显示地址和端口
    
    async with svr:
        await svr.serve_forever()
    
async def TestSendNotification():
    while True:
        logger.debug("test loop run again...")
        logger.debug("sleep 10 seconds")
        await asyncio.sleep(10)
        config = "{'test': 'test content'}"
        logger.debug("send notification to all connections: %s" % config)
        MessageCenter.SendNotification(config)
        logger.debug("send notification completed...")

try:  
    loop = asyncio.get_event_loop()
    task = asyncio.gather(start_server(), TestSendNotification())
    loop.run_until_complete(task)
except KeyboardInterrupt:
    logger.info("server close by user[Press Ctl+C]")

except Exception as e:
    logger.exception("exception occur and close server", e)
