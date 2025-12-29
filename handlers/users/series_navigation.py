from loader import dp, bot
from aiogram import types, F, html
from api import navigate_series, get_series_episodes, get_episode

@dp.callback_query(F.data.startswith("series_page"))
async def series_page_handler(call: types.CallbackQuery):
    await call.answer()
    data = call.data.split(":")
    series_id = data[1]
    page = int(data[2])
    
    result = await get_series_episodes(series_id, page)
    if not result:
        await call.message.answer("❌ Xatolik!")
        return
        
    # Generate keyboard
    keyboard = []
    row = []
    for ep in result['episodes']:
        row.append(types.InlineKeyboardButton(text=f"{ep['episode_number']}-qism", callback_data=f"series_ep:{series_id}:{ep['episode_number']}"))
        if len(row) == 3: # 3 cols
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
        
    nav_row = []
    if result['has_previous']:
        nav_row.append(types.InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"series_page:{series_id}:{page-1}"))
    if result['has_next']:
        nav_row.append(types.InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"series_page:{series_id}:{page+1}"))
    
    keyboard.append(nav_row)
    markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    # Check if message has caption (video) or text
    if call.message.caption:
        await call.message.edit_caption(caption=f"📺 {result['series_title']}\nSahifa: {result['current_page']}", reply_markup=markup)
    else:
        await call.message.edit_text(text=f"📺 {result['series_title']}\nSahifa: {result['current_page']}", reply_markup=markup)

@dp.callback_query(F.data.startswith("series_ep"))
async def series_episode_handler(call: types.CallbackQuery):
    await call.answer()
    
    # Delete previous message
    try:
        await call.message.delete()
    except:
        pass

    data = call.data.split(":")
    series_id = data[1]
    episode_number = int(data[2])
    
    episode = await get_episode(series_id, episode_number)
    if not episode:
        await call.message.answer("❌ Qism topilmadi.")
        return
        
    keyboard = []
    nav_row = []
    
    # Use prev_X/next_X logic here too, to be consistent with search_movie.py
    nav_row.append(types.InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"series_nav:{series_id}:prev_{episode_number}"))
    nav_row.append(types.InlineKeyboardButton(text=f"{episode_number}-qism", callback_data="current_ep"))
    nav_row.append(types.InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"series_nav:{series_id}:next_{episode_number}"))
    
    keyboard.append(nav_row)
    keyboard.append([types.InlineKeyboardButton(text="Barcha qismlar", callback_data=f"series_page:{series_id}:1")])
    
    markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await call.message.answer_video(video=episode['file_id'], caption=episode['caption'] or f"{episode_number}-qism", reply_markup=markup)

@dp.callback_query(F.data.startswith("series_nav"))
async def series_nav_handler(call: types.CallbackQuery):
    await call.answer()
    
    # Delete previous message
    try:
        await call.message.delete()
    except:
        pass

    data = call.data.split(":")
    series_id = data[1]
    command = data[2] # Can be 'next_5', 'prev_5', or just ID? 
    # Wait, callback was: f"series_nav:{series_id}:{episode_number+1}"
    # We should change callback to use logical commands or just pass the target "next_current"
    
    # Actually, previous implementation passed target NUMBER. 
    # But now we want "next available after X".
    # So if data[2] is digits, it's specific. But we want GAP handling.
    
    # Let's change the callback structure!
    # But wait, existing buttons might be broken? No, user is just developing.
    
    # If digit: treat as specific? Or treat as "Try to find X"?
    # The requirement: "agar 2-qismdan so`ng 10-qism turgan bo`lsa xam o`sha qismga olib o`tsin"
    # So if I am at Ep 2, and click "Next", I should send `next_2`.
    
    result = await navigate_series(series_id, command)
        
    if not result:
        await call.message.answer("❌ Boshqa qism yo'q!")
        return
    
    ep_num = result['episode_number']
    
    keyboard = []
    nav_row = []
    nav_row.append(types.InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"series_nav:{series_id}:prev_{ep_num}"))
    nav_row.append(types.InlineKeyboardButton(text=f"{ep_num}-qism", callback_data="current_ep"))
    nav_row.append(types.InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"series_nav:{series_id}:next_{ep_num}"))
    
    keyboard.append(nav_row)
    keyboard.append([types.InlineKeyboardButton(text="Barcha qismlar", callback_data=f"series_page:{series_id}:1")])
    markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await call.message.answer_video(video=result['file_id'], caption=result['caption'] or f"{ep_num}-qism", reply_markup=markup)

@dp.callback_query(F.data == "current_ep")
async def current_ep_alert(call: types.CallbackQuery):
    await call.answer("Siz shu qismni ko'ryapsiz!", show_alert=True)
