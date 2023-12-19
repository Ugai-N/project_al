import asyncio

from testTG import TGClient


class Worker:
    def __init__(self, token: str, queue: asyncio.Queue, workers_qty: int): #n - кол-во воркеров
        self.tg = TGClient(token)
        self.queue = queue
        self.is_running = False
        self.workers_qty = workers_qty
        self._tasks = []

    async def handle(self, upd):
        print('test1')
        await self.tg.send_message(upd['message']['chat']['id'], upd['message']['text'])
        # await asyncio.sleep(10)
        print('test2')

    async def worker(self):
        while self.is_running:
            upd = await self.queue.get()
            # print(type(upd))
            print(upd['message']['chat']['id'])
            print(upd['message']['text'])
            await self.handle(upd)
            self.queue.task_done() #чтобы однозначно убрать из списка unfinished???

    async def start(self):
        self.is_running = True
        for _ in range(self.workers_qty):
            task = asyncio.create_task(self.worker())
            self._tasks.append(task)

    async def stop(self):
        self.is_running = False
        await self.queue.join()
        #ждет пока очередь не станет пустой. Если мы прервем выполнение на моменте, когда там будут еще задачи, то они исчезнут навсегда и так и не будут отработаны. Поэтому лучше дождаться их выполнения
        #почитать про джоин тут https://docs.python.org/3/library/asyncio-queue.html#asyncio.Queue.join
        for task in self._tasks:
            task.cancel()
