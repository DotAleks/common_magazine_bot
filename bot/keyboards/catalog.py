from math import ceil

from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from database.models.category import Gender


def get_gender_kb() -> InlineKeyboardMarkup:
    """"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Мужской', callback_data=Gender.MALE.value), InlineKeyboardButton(text='Женский', callback_data=Gender.FEMALE.value)]
        ]
    )

class CategoryPaginationData(CallbackData, prefix='category_pagination'):
    page: int

class ProductPaginationData(CallbackData, prefix='product_pagination'):
    page: int

class CategorySelectionData(CallbackData, prefix='category_selection'):
    id: int

class AddToCartPagination(CallbackData, prefix='addToCart'):
    id: int

def get_categories_kb(categories: dict, page: int = 0) -> InlineKeyboardMarkup:
    """"""
    ITEM_PER_PAGE: int = 5

    builder = InlineKeyboardBuilder()

    items = list(categories.items())
    count_items: int = len(items)
    count_pages: int = ceil(count_items/ITEM_PER_PAGE)

    start_index: int = page*ITEM_PER_PAGE
    end_index: int = start_index+ITEM_PER_PAGE

    for id, category in items[start_index:end_index]:
        builder.button(text=category, callback_data=CategorySelectionData(id=id).pack())

    pagination_buttons = []

    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(
                text='Назад', 
                callback_data=CategoryPaginationData(page=page-1).pack()
            )
        )

    pagination_buttons.append(
        InlineKeyboardButton(
            text=f'{page + 1}/{count_pages}', 
            callback_data='current_page'
        )
    )

    if page < count_pages - 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                text='Вперёд', 
                callback_data=CategoryPaginationData(page=page+1).pack()
            )
        )

    builder.row(*pagination_buttons)
    pattern = *[1]*ITEM_PER_PAGE,3
    if page+1 == count_pages:
        count_items_per_last_page = count_items-page*ITEM_PER_PAGE
        pattern = *[1]*count_items_per_last_page,3
    
    builder.adjust(*pattern)
    return builder.as_markup()

def get_products_kb(products: dict, page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    items_list = list(products.items())
    if page < len(items_list):
        product_id, product_data = items_list[page]
    
    count_pages: int = len(products.items())
    
    pagination_buttons = []
    builder.button(text='Добавить в корзину',callback_data=AddToCartPagination(id=product_id))
    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(
                text='Назад', 
                callback_data=ProductPaginationData(page=page-1).pack()
            )
        )

    pagination_buttons.append(
        InlineKeyboardButton(
            text=f'{page + 1}/{count_pages}', 
            callback_data='current_page'
        )
    )

    if page < count_pages - 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                text='Вперёд', 
                callback_data=ProductPaginationData(page=page+1).pack()
            )
        )
    builder.row(*pagination_buttons)
    return builder.as_markup()