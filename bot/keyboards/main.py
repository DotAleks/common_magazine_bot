from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup


def get_main_kb() -> ReplyKeyboardMarkup:
    """"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Каталог'), KeyboardButton(text='Корзина')],
            [KeyboardButton(text='FAQ'), KeyboardButton(text='Мои заказы')]
        ],
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню:'
    )