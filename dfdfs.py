"""Импорт асинхронной фукции"""
import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message,BotCommand,InlineKeyboardMarkup,InlineKeyboardButton,CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
bot = Bot(token="7148523310:AAFxKdl288JChEn3LnOZpdebKY1gQoc1qXQ")
dp = Dispatcher()

router = Router()

class Anketa(StatesGroup):
    """"то что должно быть в анкте"""
    name = State()
    age = State()
    gender = State()

@router.message(Command("anketa"))
async def anketa_handler(msg: Message, state: FSMContext):
    """"Создание анкеты для пользователя"""
    await state.set_state(Anketa.name)
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa')]])
    await msg.answer('Введите ваше имя', reply_markup=markup)

@router.callback_query(F.data == 'cancel_anketa')
async def cancel_handler(callback_query: CallbackQuery, state: FSMContext):
    """Отмена заполнения анкеты"""
    await state.clear()
    await callback_query.message.answer('Регистрация отменена')

@router.message(Anketa.name)
async def set_name_by_anketa_handler(msg: Message, state: FSMContext):
    """Получает имя пользователя"""
    await state.update_data(name=msg.text)
    await state.set_state(Anketa.age)
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Назад', callback_data='set_name_anketa'),
        InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa')]])
    await msg.answer('Введите ваш возраст', reply_markup=markup)


@router.callback_query(F.data == 'set_name_anketa')
async def set_name_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    """Обратный запрос имя"""
    await anketa_handler(callback_query.message, state)

@router.message(Anketa.age)
async def set_age_by_anketa_handler(msg: Message, state: FSMContext):
    """Получает возраст пользователя"""
    try:
        await state.update_data(age=int(msg.text))
    except ValueError:
        await msg.answer('Вы не верно ввели возраст!')
        markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='Назад',callback_data='set_name_anketa'),
            InlineKeyboardButton(text='Отмена',callback_data='cancel_anketa')]])
        await msg.answer('Введите Ваш возраст',reply_markup=markup)
        return

    await state.set_state(Anketa.gender)
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='Мужчина',callback_data='set_man'),
            InlineKeyboardButton(text='Женщина',callback_data='set_woman')]])
    await msg.answer('Введите Ваш пол',reply_markup=markup)

@router.callback_query(F.data == 'set_man')
async def set_gender_anketa_handler1(callback_query: CallbackQuery, state: FSMContext):
    await anketa_handler(callback_query.message, state)

@router.callback_query(F.data == 'set_woman')
async def set_gender_anketa_handler2(callback_query: CallbackQuery, state: FSMContext):
    await anketa_handler(callback_query.message, state)


@router.callback_query(F.data =='set_age_anketa')
async def set_age_anketa_handler(callback_query:CallbackQuery,state:FSMContext):
    await state.set_state(Anketa.age)
    markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='Назад',callback_data='set_name_anketa'),
            InlineKeyboardButton(text='Отмена',callback_data='cancel_anketa')]])
    await callback_query.message.answer('Введите Ваш возраст', reply_markup=markup)

@router.message(Anketa.gender)
async def set_ag_by_anketa_handler(msg:Message,state: FSMContext):
    """"""
    await state.update_data(gender = msg.text)
    await msg.answer(str(await state.get_data()))
    await state.clear()

@router.message(Command("start"))
async def start_handler(msg: Message):
    """Обработка команды старт"""
    await bot.set_my_commands([
        BotCommand(command='start', description='Запуск бота'),
        BotCommand(command='help', description='Справка'),
        BotCommand(command='delete', description='Отчислиться'),
    ])

    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вперёд', callback_data='next')]
    ])
    await msg.answer(text="Страница 1", reply_markup=inline_markup)

@router.callback_query(F.data == 'next')
async def next_handler(callback_query: CallbackQuery):
    """метод возвращающий к предыдущему действию"""
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back')]

    ])

    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Страница 2',
        reply_markup=inline_markup)

@router.callback_query(F.data == 'back')
async def back_handler(callback_query: CallbackQuery):
    """Копка отправляющая пользователя на действие вперед"""
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вперёд', callback_data='next')]
    ])

    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Страница 1', 
        reply_markup=inline_markup)

async def main():
    """запуск бота"""
    await dp.start_polling(bot)
dp.include_routers(router)

if __name__ == '__main__':
    asyncio.run(main())