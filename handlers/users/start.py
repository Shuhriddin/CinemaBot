from keyboards.inline.buttons import share_button
from loader import dp,bot
from aiogram import types,F,html
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardButton
from utils.misc.subscription import check
from middlewares.mymiddleware import CheckSubscriptionCallback
from api import *
import os
from data.config import *
def text(fullname):
    return (f"👋 Assalomu alaykum {html.bold(fullname)}!\n\n"
            f"😊 {html.italic('Kinoteatr botimizga xush kelibsiz!')}\n"
            f"🔎 {html.bold(' Kino qidirish uchun shunchaki kino nomini yozib yuboring!')}\n"
            f"<i>🔢 Agar kinoni kodi orqali qidiriyotgan bo'lsangiz kino kodini yozib yuboring!</i>\n"
            f"<b>⬆️ /top buyrug'i orqali Top 5 kinoni ko'rishingiz mumkin!</b>")
subs ='''
Iltimos bot to'liq ishlashi uchun quyidagi kanallarga obuna bo'ling!
'''
import sqlite3
@dp.message(CommandStart())
async def start_chat(message:types.Message):
    try:
        await create_user(name=message.from_user.full_name,telegram_id=message.from_user.id)
    except Exception as e:
        print(e)
    btn = InlineKeyboardBuilder()
    final_status = True
    channels = await get_all_channels()
    if channels:
        for channel in await get_all_channels():
            status = True
            try:
                status = await check(user_id=message.from_user.id,
                                     channel=channel['channel_id'])
            except:
                pass
            final_status *= status
            try:
                channel = await bot.get_chat(channel['channel_id'])
            except Exception as e:
                print(e)
                pass
            if not status:
                invite_link = await channel.export_invite_link()
                btn.row(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))
        btn.button(text='Obunani tekshirish', callback_data=CheckSubscriptionCallback(check=True))
        btn.adjust(1)
        if final_status:
            await message.answer(text=text(message.from_user.full_name),reply_markup=share_button())
        if not final_status:
            await message.answer(text= subs,
                                 reply_markup=btn.as_markup(row_width=1))
    else:
            await message.answer(text=text(message.from_user.full_name),reply_markup=share_button())
@dp.callback_query(CheckSubscriptionCallback.filter())
async def test(call:types.CallbackQuery):
    await call.answer(cache_time=60)
    k = []
    final_status = False
    user_id = call.from_user.id
    kanallar =await get_all_channels()
    for kanal in kanallar:
        try:
            channel = await bot.get_chat(kanal['channel_id'])
        except:
            pass
        try:
            res = await bot.get_chat_member(chat_id=kanal['channel_id'], user_id=user_id)
        except:
            continue
        if res.status == 'member' or res.status == 'administrator' or res.status == 'creator':
            k.append(InlineKeyboardButton(text=f"✅ {channel.title}", url=f"{await channel.export_invite_link()}"))

        else:
            k.append(InlineKeyboardButton(text=f"❌ {channel.title}", url=f"{await channel.export_invite_link()}"))
            final_status = True
    builder = InlineKeyboardBuilder()
    builder.add(*k)
    builder.button(text='Obunani tekshirish', callback_data=CheckSubscriptionCallback(check=True))
    builder.adjust(1)
    if final_status:
        await bot.send_message(chat_id=user_id,
                               text=subs,
                               reply_markup=builder.as_markup())
    else:
        await call.message.answer(text(call.from_user.full_name),reply_markup=share_button())
    await call.message.delete()
