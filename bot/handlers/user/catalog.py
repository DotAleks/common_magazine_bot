from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_gender_kb, get_categories_kb, get_products_kb
from database.repositories import CategoryRepository, ProductRepository
from database import Database
from bot.keyboards.catalog import CategorySelectionData, CategoryPaginationData, ProductPaginationData

router = Router(name='user_catalog')

@router.message(F.text == 'Каталог')
async def handle_catalog(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state('gender')
    await message.answer(text='Выберите пол:',reply_markup=get_gender_kb())

@router.callback_query(F.data.in_(['MALE','FEMALE']))
async def handle_gender(callback: CallbackQuery, state: FSMContext, database: Database) -> None:
    if callback.data is None:
        await callback.answer("Ошибка: нет данных в кнопке")
        return
    
    gender = callback.data
    
    await state.update_data(gender=gender)
    
    category_repo = CategoryRepository(database)
    #TODO: Добавить в кеш redis на db=1
    category_objects = await category_repo.get_by_gender(gender=gender)

    categories: dict = {category.id: category.name for category in category_objects}

    if isinstance(callback.message, Message):
        await callback.message.edit_text(text='Выберите категорию: ', reply_markup=get_categories_kb(categories=categories))
        await callback.answer()


@router.callback_query(CategoryPaginationData.filter())
async def handle_category_nav(callback: CallbackQuery, callback_data: CategoryPaginationData, database: Database, state: FSMContext) -> None:
    page = callback_data.page
    data = await state.get_data()
    gender = data['gender']

    category_repo = CategoryRepository(database)
    #TODO: Брать из кеша redis db=1
    category_objects = await category_repo.get_by_gender(gender=gender)
    categories: dict = {category.id: category.name for category in category_objects}
    if isinstance(callback.message, Message):
        await callback.message.edit_text(text='Выберите категорию: ', reply_markup=get_categories_kb(page=page,categories=categories))
        await callback.answer()

@router.callback_query(CategorySelectionData.filter())
async def handle_product(callback: CallbackQuery, callback_data: CategorySelectionData, database: Database, state: FSMContext) -> None:
    category_id = callback_data.id
    await state.set_state('category_id')
    await state.update_data(category_id=category_id)# Поменять на кеш

    product_repo = ProductRepository(database)
    product_objects = await product_repo.get_by_category_id(category_id=category_id)
    
    products: dict = {product_object.id: [product_object.name, product_object.counts, product_object.sizes, product_object.price, product_object.image_url] for product_object in product_objects}

    first_key = next(iter(products))
    first_value = products[first_key]
    text = f"""{first_value[0]}
Осталось: {first_value[1]} шт.
{first_value[3]} Р
            """
    media: InputMediaPhoto = InputMediaPhoto(media=first_value[-1], caption=text)
    if isinstance(callback.message, Message):
        await callback.message.edit_media(media=media,reply_markup=get_products_kb(products=products))
        await callback.answer()
    
@router.callback_query(ProductPaginationData.filter())
async def handle_product_nav(callback: CallbackQuery, callback_data: ProductPaginationData, database: Database, state: FSMContext) -> None:
    page = callback_data.page
    data = await state.get_data()
    category_id: int = data['category_id']
    product_repo = ProductRepository(database)
    product_objects = await product_repo.get_by_category_id(category_id=category_id)
    
    products: dict = {product_object.id: [product_object.name, product_object.counts, product_object.sizes, product_object.price, product_object.image_url] for product_object in product_objects}

    first_key = next(iter(products))
    first_value = products[first_key+page]
    text = f"""{first_value[0]}
Осталось: {first_value[1]} шт.
{first_value[3]} Р
            """
    media: InputMediaPhoto = InputMediaPhoto(media=first_value[-1], caption=text)
    if isinstance(callback.message, Message):
        await callback.message.edit_media(media=media,reply_markup=get_products_kb(products=products, page=page))
        await callback.answer()