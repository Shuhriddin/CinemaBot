from typing import Union
from loader import bot
async def check(user_id, channel: Union[str,int]):
    member = await bot.get_chat_member(chat_id=channel,user_id=user_id)
    if member.status=='member' or member.status=='administrator' or member.status=='creator':
        return True
    else:
        return False