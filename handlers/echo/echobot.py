from loader import dp
from aiogram import types,F
from filters import IsPrivate
from keyboards.inline.buttons import share_button
from api import *
from handlers.users.start import text
@dp.message(IsPrivate())
async def echo_bot(message:types.Message):
    await message.answer(text(message.from_user.full_name),reply_markup=share_button())
