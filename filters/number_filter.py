from aiogram.filters import Filter
from aiogram import types

class MovieCodeFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.text.isdigit()