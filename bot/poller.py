import asyncio

from testTG import TGClient


class Poller:
    def __init__(self, token: str, queue: asyncio.Queue):
        self.tg = TGClient(token)
        self.queue = queue
        self.is_running = False
        self._task = None

    async def getter(self):
        offset = 0
        while self.is_running:
            try:
                updates = await self.tg.get_updates(offset=offset, timeout=60)
            except KeyboardInterrupt:
                pass
            # except asyncio.CancelledError:
            #     print('CancelledError')
            print(len(updates['result']))

            for upd in updates['result']:
                self.queue.put_nowait(upd)
                print(upd['update_id'])
                # print(upd['message']['chat'])
                offset = upd['update_id'] + 1
                # offset += 1

    async def start(self):
        print('started')
        self.is_running = True
        self._task = asyncio.create_task(self.getter())

    async def stop(self):
        self.is_running = False
        self._task.cancel()
        print('stop')

