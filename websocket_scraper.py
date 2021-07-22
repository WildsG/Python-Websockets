from abc import ABCMeta, abstractmethod
import websockets
import traceback
import os


class WebsocketScraper(metaclass=ABCMeta):

    def __init__(self) -> None:
        process_name = "[Process %s]" % (os.getpid())
        print("%s Started " % process_name)

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def _consume(self, message: str) -> None:
        pass

    async def _websocket_connect(self, uri: str, payload: str) -> None:
        websocket = await websockets.connect(uri, ping_interval=None)
        await websocket.send(payload)
        # TODO implement some kind of exponential back-off for reconnecting
        while True:
            if not websocket.open:
                try:
                    print('Websocket is NOT connected. Reconnecting...')
                    websocket = await websockets.connect(uri, ping_interval=None)
                    await websocket.send(payload)
                    print('Connected to ' + uri)
                except:
                    print('Unable to reconnect, trying again.')
            try:
                async for message in websocket:
                    if message is not None:
                        self._consume(message)
            except:
                print('Error receiving message from websocket.')
                traceback.print_exc()



