import asyncio
import os

from poller import Poller
from bot import Bot
from worker import Worker

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
workers_qty = 2
# TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
#
# async def fetch():
#     c = TGClient(TELEGRAM_TOKEN)
#     # c = TGClient(f"{os.environ.get('TELEGRAM_TOKEN')}")
#     # print(f"{os.environ.get('TELEGRAM_TOKEN')}")
#     print(await c.get_updates(offset=602586536, timeout=5)) #offset - id update-a с какого начинать


# async def start():
#     bot = Bot(TELEGRAM_TOKEN, workers_qty)
#     await bot.start()
#     return bot


def run():
    # asyncio.get_event_loop().run_until_complete(fetch())
    loop = asyncio.get_event_loop()
    bot = Bot(TELEGRAM_TOKEN, workers_qty)
    try:
        loop.create_task(bot.start())

        # bot = loop.run_until_complete(start())
    # queue = asyncio.Queue()
    # poller = Poller(TELEGRAM_TOKEN, queue)
    # worker = Worker(TELEGRAM_TOKEN, queue, 1)
    # loop.create_task(poller.start())
    # loop.create_task(worker.start())
        loop.run_forever()
    except KeyboardInterrupt:
        print('already stopping')
        loop.run_until_complete(bot.stop())
        print('has been stopped')

if __name__ == '__main__':
    run()