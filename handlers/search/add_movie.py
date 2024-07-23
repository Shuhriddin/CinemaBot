from loader import dp
from aiogram import F,types,html
from api import create_movie
from data.config import DB_TG_CHANNEL
@dp.channel_post(F.video)
async def add_movie_todb(message:types.Message):
    if str(message.chat.id) == str(DB_TG_CHANNEL):
        data = await create_movie(description=message.caption,file_id=message.video.file_id)
        if data == 'Yuklanmadi!':
            await message.reply(html.bold("✅ Kino allaqachon bazda bor."))
        else:
            await message.reply(html.bold("✅ Kino bazaga yuklandi.\n"
                                          f"🔎 Kino kodi:{html.bold(html.code(data))}"))
    else:
        pass
