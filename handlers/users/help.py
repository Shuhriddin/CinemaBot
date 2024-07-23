from aiogram.filters import Command
from loader import dp
from aiogram import types,html
@dp.message(Command('help'))
async def help_bot(message:types.Message):
    await message.answer(
        f"{html.bold('😊 Sizga qanday yordam berishim mumkin?')}\n\n"
        f"{html.bold('🔎 Kino qidirish uchun kino nomi yozing yoki kino kodini yuboring.')}"
    )