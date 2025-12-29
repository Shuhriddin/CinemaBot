from aiogram import Router, F, types, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from api import create_movie, add_episode
from states.series_state import SeriesState
from loader import dp, bot
from data.config import ADMINS

@dp.message(Command("newseries"), F.chat.id.in_(ADMINS))
async def new_series_handler(message: types.Message, state: FSMContext):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("⚠️ Serial nomini kiriting!\nMisol: /newseries Kurtlar Vadisi")
        return

    title = args[1]
    
    # Create Series in Backend
    result = await create_movie(description=title, is_series=True)
    
    if result == "Yuklanmadi!":
        await message.reply("❌ Xatolik yuz berdi.")
        return

    await state.update_data(series_id=result)
    await state.set_state(SeriesState.uploading_episodes)
    
    await message.reply(f"✅ <b>{title}</b> seriali yaratildi!\n"
                        f"🆔 Kodi: {html.code(result)}\n\n"
                        f"Endi qismlarni yuboring (fayl formatida). Tugatgach /stop bosing.")

@dp.message(Command("addepisode"), F.chat.id.in_(ADMINS))
async def add_episode_cmd(message: types.Message, state: FSMContext):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("⚠️ Serial kodini kiriting!\nMisol: /addepisode 210")
        return

    series_id = args[1]
    
    # Optionally verify if series exists here, but for now just trust admin
    await state.update_data(series_id=series_id)
    await state.set_state(SeriesState.uploading_episodes)
    
    await message.reply(f"✅ Serial ID: {series_id} tanlandi.\n"
                        f"Endi qismlarni yuboring. Tugatgach /stop bosing.")


@dp.message(SeriesState.uploading_episodes, F.video)
async def upload_episode_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    series_id = data.get('series_id')
    
    file_id = message.video.file_id
    caption = message.caption
    
    result = await add_episode(series_id=series_id, file_id=file_id, caption=caption)
    
    if result:
        ep_num = result.get('episode_number')
        await message.reply(f"✅ {ep_num}-qism qo'shildi!")
    else:
        await message.reply("❌ Qism qo'shishda xatolik!")

@dp.message(Command("stop"), SeriesState.uploading_episodes)
async def stop_upload(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("✅ Yuklash to'xtatildi.")
