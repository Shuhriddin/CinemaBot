import handlers,middlewares
from loader import dp,bot
import asyncio
from utils.notify_admins import start,shutdown
from utils.set_botcommands import private_chat_commands
from middlewares.mymiddleware import UserCheckMiddleware
# Info
import logging
import sys
async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await private_chat_commands()
        dp.startup.register(start)
        dp.shutdown.register(shutdown)
        dp.message.middleware(UserCheckMiddleware())
        # try:
        #     db.create_table_channels()
        #     db.create_table_users()
        # except:
        #     pass
        #############################
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Goodbye!')