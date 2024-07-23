from loader import dp,bot
from aiogram import types,F
from filters import *
from states.mystate import AddChannelState
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from api import get_all_channels,get_channel
from keyboards.default.buttons import back_button,admin_button
class InfoChannelCallback(CallbackData,prefix='behzod'):
    id:str
@dp.message(F.text=="🗣 Kanallar",IsChatAdmin(),IsPrivate())
async def start_add_channel(message:types.Message,state:FSMContext):
    CHANNELS =await get_all_channels()
    btn = InlineKeyboardBuilder()
    for channel  in CHANNELS:
        try:
            kanal = await bot.get_chat(chat_id=channel['channel_id'])
            title = kanal.title
            btn.button(text=f"{title}", callback_data=InfoChannelCallback(id=channel['channel_id']))
            btn.adjust(1)
        except Exception as e:
            pass
    if CHANNELS:
        await message.answer("Ma'lumot olmoqchi bo'lgan kanaliz ustiga bosing!", reply_markup=btn.as_markup())
    else:
        await message.answer("Kanal topilmadi!")
@dp.callback_query(InfoChannelCallback.filter(),IsChatAdmin())
async def get(call:types.CallbackQuery,callback_data:InfoChannelCallback,state:FSMContext):
    channel_id = callback_data.id
    await call.answer(cache_time=60)
    try:
        channel = await get_channel(channel_id=channel_id)
        subscribers = await bot.get_chat_member_count(chat_id=channel_id)
        await call.message.answer(f"Kanal nomi: {channel['channel_name']}\n"\
            f"Kanal obunachilar soni: {subscribers}")
    except:
        pass 
    await call.message.delete()



