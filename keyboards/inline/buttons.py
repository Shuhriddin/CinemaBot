from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
class MovieCallBack(CallbackData,prefix='movie'):
    id:str
class PaginatorCallback(CallbackData,prefix='page'):
    action:str
    page:int
    length:int
class Format(CallbackData,prefix='ikb0000'):
    choose:str
class LanguageCallback(CallbackData,prefix='ikb0001'):
    language:str
def text_format(choose=None):
    choose = 'TEXT' if choose==None else choose
    btn  = InlineKeyboardBuilder()
    btn.button(text=f"Markup format: {choose}",callback_data=Format(choose=choose))
    return btn.as_markup()
page_size=5
def pagination_btn(data,page:int=0):
    btn = InlineKeyboardBuilder()
    length = len(data)
    data = data
    try:
        start = page * page_size
        finish = (page + 1) * page_size
        if finish > length:
            datas = data[start:length]
        else:
            datas = data[start:finish]
    except:
        pass
    counter = 1
    for i in datas:
        btn.row(
            InlineKeyboardButton(text=f"{counter}", callback_data=MovieCallBack(id=str(i['id'])).pack()),
            width=5
        )
        counter+=1
    btn.adjust(len(datas))
    btn.row(
        InlineKeyboardButton(text='⬅️',
                             callback_data=PaginatorCallback(action='prev', page=page, length=length).pack()),
        InlineKeyboardButton(text='❌',
                             callback_data=PaginatorCallback(action='delete', page=page, length=length).pack()),
        InlineKeyboardButton(text='➡️', callback_data=PaginatorCallback(action='next', page=page, length=length).pack())
    )
    return btn.as_markup()


def share_button():
    btn = InlineKeyboardBuilder()
    btn.button(text="🎥 Ulashish 🎥",
               switch_inline_query="Kinoteatr bot bilan istalgan filmizni topishingiz mumkin!!!")
    btn.adjust(1)
    return btn.as_markup()
