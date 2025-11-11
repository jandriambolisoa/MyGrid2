import asyncio
from typing import Callable


class Signal:
    def __init__(self, name):
        self.name = name
        self.listeners = dict()

    def connect(self, func: Callable):
        if not func.__name__ in self.listeners:
            self.listeners[func.__name__] = func

        else:
            raise ValueError(f"Function {func.__name__} is already connected.")

    async def send(self, *args, **kwargs):

        for func in self.listeners:
            await self.listeners[func](*args, **kwargs)
