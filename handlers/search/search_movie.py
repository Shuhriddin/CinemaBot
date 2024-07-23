from loader import dp,bot
from aiogram import types,F,suppress,html
from aiogram.exceptions import TelegramBadRequest
from api import *
from aiogram.filters import CommandObject,Command
from filters import MovieCodeFilter
from aiogram.fsm.context import FSMContext
from keyboards.inline.buttons import *
caption=html.bold("🎬 Istalgan kino mavjud bo'lgan bot: ")
@dp.message(F.text,MovieCodeFilter())
async def get_movie_code(message:types.Message):
    try:
        movie = await search_movie_code(code=message.text)
        await movie_rate(code=message.text)
        bot_me = await bot.get_me()
        username = bot_me.username
        try:
            await message.answer_document(document=movie['file_id'],
                                          caption=
                                          f"Kino haqida:👇👇👇\n"
                                          f"{movie['description']}\n\n"
                                          f"{caption}@{username}", reply_markup=share_button())
        except Exception as e:
            print(f"bu {e}")
            await message.answer("Kino topilmadi!")
    except:
        await message.answer("Kino topilmadi!")
@dp.message(Command('top'))
async def get_movies_by_search(message:types.Message,state:FSMContext):
            results = await top_movies()
            if results:
                await state.update_data({
                    'data': results
                })
                length = len(results)
                if results:
                    page = 0
                    next = (page + 1) * page_size if length > (page + 1) * page_size else length
                    text1 = f"Natijalar 1-{next} {length} dan"
                    text2 = ''
                    counter = 1
                    for i in results[page:next]:
                        text2 += f"{counter}.{i['description']}" + '\n'
                        counter += 1
                    text1 += '\n' + text2
                    await message.answer(text=text1, reply_markup=pagination_btn(data=results, page=page))
            else:
                await message.answer(
                    f"{html.bold('Bazada kino topilmadi!')}"
                )

@dp.message(Command('kino'))
async def get_movie_code(message:types.Message,command:CommandObject):
    id = command.args
    movie = await search_movie_code(code=id)
    await movie_rate(code=id)
    bot_me = await bot.get_me()
    username = bot_me.username
    try:
        await message.answer_document(document=movie['file_id'],
                                           caption=
                                           f"Kino haqida:👇👇👇\n"
                                           f"{movie['description']}\n\n"
                                           f"{caption}@{username}",reply_markup=share_button())
    except Exception as e:
        print(e)
        await message.answer("Kino topilmadi!")

@dp.message(F.text,~MovieCodeFilter())
async def get_movies_by_search(message:types.Message,state:FSMContext):
    if len(message.text)<20:
        search = await search_movie(message.text)
        if search==[]:
                await message.answer("Afsuski u nom bilan kino topilmadi!")
        else:
            results = await search_movie(message.text)
            await state.update_data({
                'data': results
            })
            length = len(results)
            if results:
                page = 0
                next = (page + 1) * page_size if length > (page + 1) * page_size else length
                text1 = f"Natijalar 1-{next} {length} dan"
                text2 = ''
                counter = 1
                for i in results[page:next]:
                    text2 += f"{counter}.{i['description']}" + '\n'
                    counter += 1
                text1 += '\n' + text2
                await message.answer(text=text1, reply_markup=pagination_btn(data=results, page=page))
    else:
            await message.answer("Kino qidirishda eng ko'pi 10 ta belgidan foydalaning!")

@dp.callback_query(PaginatorCallback.filter())
async def change_size(call:types.CallbackQuery,callback_data:PaginatorCallback,state:FSMContext):
    page = int(callback_data.page)
    action = callback_data.action
    length = int(callback_data.length)
    data = await state.get_data()
    results = data['data']
    if action == 'delete':
        await call.message.delete()
    else:
        if action == 'next':
            if (page + 1) * page_size >= length:
                await call.answer("Eng oxirgi sahifadasiz...")
                page = page
            else:
                page = page + 1
        else:
            if page > 0:
                page = page - 1
            else:
                await call.answer("Eng oldingi sahifadasiz...")
                page = page
        start = page * page_size
        start_t = (page + 1) if page <= 0 else page * page_size
        finish = (page + 1) * page_size if length > (page + 1) * page_size else length
        text1 = f"Natijalar {start_t}-{finish} {length} dan"
        text2 = ''
        counter = 1
        for i in results[start:finish]:
            text2 += f"{counter}.{i['description']}" + '\n'
            counter += 1
        text1 += '\n' + text2
        with suppress(TelegramBadRequest):
            await call.message.edit_text(text=text1, reply_markup=pagination_btn(data=results, page=page))
@dp.callback_query(MovieCallBack.filter())
async def get_movie(call:types.CallbackQuery,callback_data:MovieCallBack,state:FSMContext):
    id = int(callback_data.id)
    await call.answer(cache_time=60)
    movie = await get_film(id=id)
    bot_me = await bot.get_me()
    username = bot_me.username
    try:
        await call.message.answer_document(document=movie['file_id'],
                                           caption=
                                           f"Kino haqida:👇👇👇\n"
                                           f"{movie['description']}\n\n"
                                           f"{caption}@{username}",reply_markup=share_button())
        await movie_rate(code=id)
    except:
        await call.message.answer(f'{html.bold("Kino topilmadi!")}')

