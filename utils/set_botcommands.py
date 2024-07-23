from aiogram import types
from loader import bot
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats
async def private_chat_commands():
    commands = [
        types.BotCommand(command='start', description="Restart bot"),
        types.BotCommand(command='help', description="Yordam"),
        types.BotCommand(command='top',description="Top 5 kino")
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats(type='all_private_chats')
    )