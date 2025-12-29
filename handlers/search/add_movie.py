from loader import dp
from aiogram import F,types,html
from api import create_movie
from data.config import DB_TG_CHANNEL
import re
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


def parse_caption(caption: str):
    # Pattern to match "number-qism", "number qism", "numberqism"
    episode_match = re.search(r'(\d+)[-\s]*qism', caption, re.IGNORECASE)
    
    # Try to find "Kino nomi: Title"
    name_match = re.search(r'Kino nomi:?\s*([^\n\r|➖]+)', caption, re.IGNORECASE)
    
    if name_match:
        title = name_match.group(1).strip()
        # Remove episode number pattern from title if present
        if episode_match:
            title = title.replace(episode_match.group(0), '').strip()
        # Clean title from common emojis and special chars
        title = re.sub(r'[^\w\s\']+', '', title).strip()
    else:
        # Fallback: take first line and clean it
        title = caption.split('\n')[0].strip()
        if episode_match:
            title = title.replace(episode_match.group(0), '').strip()
        title = re.sub(r'\s+', ' ', title).strip(' ()[]-')

    if episode_match:
        episode_number = int(episode_match.group(1))
        return title, episode_number, True
        
    return title, None, False

@dp.channel_post(F.video)
async def add_movie_todb(message:types.Message):
    if str(message.chat.id) == str(DB_TG_CHANNEL):
        caption = message.caption or "Nomsiz media"
        title, episode_number, is_series = parse_caption(caption)
        
        data = await create_movie(
            description=title,
            file_id=message.video.file_id,
            is_series=is_series,
            episode_number=episode_number,
            caption=caption
        )
        
        if data == 'Yuklanmadi!':
            await message.reply(html.bold("❌ Xatolik yuz berdi yoki kino oldin yuklangan."))
        else:
            msg = f"✅ Media bazaga yuklandi.\n🔎 Kod: {html.bold(html.code(data))}\nNomi: {title}"
            if is_series:
                msg += f" ({episode_number}-qism)"
            await message.reply(msg)
    else:
        pass
