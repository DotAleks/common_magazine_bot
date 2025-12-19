from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_gender_kb, get_categories_kb
from database.repositories import CategoryRepository
from database import Database
from database.models.category import Gender
from bot.keyboards.catalog import CategorySelectionData, CategoryPaginationData

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
    data = await state.get_data()
    gender = data['gender']
    category_id = callback_data.id
