from data.config import ADMINS
from loader import dp,bot
from  aiogram import types,F
from filters import *
from aiogram.filters import Command
from keyboards.default.buttons import *
from keyboards.inline.buttons import *
from states.mystate import TextState
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from helper import check_url
@dp.message(F.text=='📝 Tekst',IsChatAdmin(),IsPrivate())
async def start_create_text_post(message:types.Message,state:FSMContext):
        await message.answer("<b>Post tekstini yuboring.</b>",reply_markup=back_button())
        await message.answer("Post sozlamalari:",reply_markup=text_format())
        await state.set_state(TextState.text)
@dp.callback_query(Format.filter(),IsChatAdmin())
async def change_format(call:types.CallbackQuery,callback_data:Format,state:FSMContext):
    choose = 'TEXT' if callback_data.choose=='HTML' else 'HTML'
    await state.update_data({
        'choose':choose
    })
    await call.message.edit_reply_markup(reply_markup=text_format(choose))
@dp.message(F.text=='◀️ Orqaga',IsChatAdmin(),TextState.text,IsPrivate())
async def get_add_type(message:types.Message,state:FSMContext):
    await message.answer("Qaysi turdagi xabar yuborasiz!\n"
                         "Tanlang👇",reply_markup=add_type())
    await state.clear()

@dp.message(TextState.text,IsChatAdmin(),IsPrivate())
async def get_text(message:types.Message,state:FSMContext):
    content_type = message.content_type
    if content_type=='text':
            await state.update_data({
                'text':message.text,
                'type':'text'
            })

            text="Havolani quyidagi formatda yuborish:\n" \
                       "[tugma matni+havola]\n" \
                       "<i>Misol:\n</i>" \
                       "[Tarjimon+https://t.me/Behzod_Asliddinov]\n" \
                       "Bir qatorga bir nechta tugmalar qo'shish uchun yangi qatorga yangi havolalarni yozing.\n" \
                       "<i>Format:\n</i>" \
                       "[Birinchi matn+birinchi havola]\n" \
                       "[Ikkinchi matn+ikkinchi havola]\n"
            await message.answer(text=message.text)
            await message.answer(text,reply_markup=need_or_not())
            await state.set_state(TextState.url)
    else:
            await message.answer("<b>Post tekstini yuboring.</b>", reply_markup=back_button())
            await message.answer("Post sozlamalari:", reply_markup=text_format())
            await state.set_state(TextState.text)
@dp.message(F.text=="🆗 Kerakmas",TextState.url,IsChatAdmin(),IsPrivate())
async def pass_to_url(message:types.Message,state:FSMContext):
    data = await state.get_data()
    await message.answer(text=data['text'])
    await message.answer("Agar tayyor bo'lsa '📤 Yuborish' tugmasini bosing!", reply_markup=send())
    await state.set_state(TextState.check)
# Cancel
@dp.message(F.text=="⏺ Bekor qilish",TextState.url,IsChatAdmin(),IsPrivate())
async def pass_to_url(message:types.Message,state:FSMContext):
        await message.answer("Qaysi turdagi xabar yuborasiz!\n"
                             "Tanlang👇", reply_markup=add_type())
        await state.clear()
# Cancel 2
@dp.message(F.text=="⏺ Bekor qilish",TextState.check,IsChatAdmin(),IsPrivate())
async def pass_to_url(message:types.Message,state:FSMContext):
        await message.answer("Qaysi turdagi xabar yuborasiz!\n"
                             "Tanlang👇", reply_markup=add_type())
        await state.clear()
@dp.message(TextState.url,IsChatAdmin(),IsPrivate())
async def get_link(message:types.Message,state:FSMContext):
    if message.content_type=='text':
        link = message.text
        urls = check_url(link)
        urls = urls if urls else None
        await state.update_data({
            'buttons': urls
        })
        data = await state.get_data()
        links  = urls.splitlines()
        btn  = InlineKeyboardBuilder()
        for link in links:
            manzil = link[link.rfind('+') + 1:]
            manzil = manzil.strip()
            text = link[:link.rfind('+')]
            text = text.strip()
            btn.button(text=text, url=manzil)
        btn.adjust(1)
        await message.answer(text=data['text'],reply_markup=btn.as_markup())
        await message.answer("Agar tayyor bo'lsa '📤 Yuborish' tugmasini bosing!",reply_markup=send())
        await state.set_state(TextState.check)
    else:
            text = "Havolani quyidagi formatda yuborish:\n" \
                   "[tugma matni+havola]\n" \
                   "<i>Misol:\n</i>" \
                   "[Tarjimon+https://t.me/Behzod_Asliddinov]\n" \
                   "Bir qatorga bir nechta tugmalar qo'shish uchun yangi qatorga yangi havolalarni yozing.\n" \
                   "<i>Format:\n</i>" \
                   "[Birinchi matn+birinchi havola]\n" \
                   "[Ikkinchi matn+ikkinchi havola]\n"
            await message.answer(text=message.text)
            await message.answer(text, reply_markup=need_or_not())
            await state.set_state(TextState.url)
@dp.message(F.text=="📤 Yuborish",TextState.check,IsChatAdmin(),IsPrivate())
async def check_post(message:types.Message,state:FSMContext):
    data = await state.get_data()
    from api import get_all_users
    USERS = await get_all_users()
    if data.get('buttons',None):
        links = data['buttons'].splitlines()
        btn = InlineKeyboardBuilder()
        for link in links:
            manzil = link[link.rfind('+') + 1:]
            manzil = manzil.strip()
            text = link[:link.rfind('+')]
            text = text.strip()
            btn.button(text=text,url=manzil)
        btn.adjust(1)
        counter = 0
        for i in USERS:
            try:
                await bot.send_message(text=data['text'], chat_id=i['telegram_id'],reply_markup=btn.as_markup(row_width=1))
                counter+=1
            except Exception as e:
                print(e)
        await message.answer(f"{counter} kishiga xabar yuborildi!", reply_markup=admin_button())
    else:
        text = data['text']
        counter = 0
        for i in USERS:
            try:
                await bot.send_message(text=text, chat_id=i['telegram_id'])
                counter+=1
            except Exception as e:
                print(e)
        await message.answer(f"{counter} kishiga xabar yuborildi!",reply_markup=admin_button())
    await state.clear()
