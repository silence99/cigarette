import asyncio
import utils.LogMgr as log
from notification.agent import Agent
from notification.center import MessageCenter
import notification.configListenser as listener
import threading
from settings import options

logger = log.GetLogger()

async def start_server(addr='localhost', port=8080):
    loop = asyncio.get_running_loop()
    svr = await loop.create_server(lambda: Agent(), addr, port)
    host = svr.sockets[0].getsockname()  # 获得这个服务器的第一个套接字的地址和端口
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))  # 在控制台中显示地址和端口

    async with svr:
        await svr.serve_forever()

def dispatch(data):
    MessageCenter.SendNotification(data)


try:
    listenThread = threading.Thread(
        target=listener.listen, args=(options, dispatch))
    listenThread.daemon = True
    
    listenThread.start()

    loop = asyncio.get_event_loop()
    task = asyncio.gather(start_server())
    loop.run_until_complete(task)
except KeyboardInterrupt:
    logger.info("server close by user[Press Ctl+C]")

except Exception as e:
    logger.exception("exception occur and close server", e)
    
    
