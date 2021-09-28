from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from datetime import datetime
from restart import Commands
import os
import sys
base_dir = os.path.abspath(os.path.join(os.path.dirname('bot_grabber.py'), '..'))
sys.path.append(base_dir)
from sqll.sql import SQL

restart_session = Commands()

TOKEN = '2022290181:AAG53Y9mvkUs-gB1KTWAjriTwn_JQv01Hx8'
USER_ID = '740725175'

db = SQL('../bd.db')
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

keyboard = InlineKeyboardMarkup(row_width=3)
donor_k = InlineKeyboardButton(text='Донор', callback_data="donor")
moder_k = InlineKeyboardButton(text='Модер', callback_data="moder")
channel_k = InlineKeyboardButton(text='Канал', callback_data="channel")
keyboard.add(donor_k, moder_k, channel_k)

donor_keyboard = InlineKeyboardMarkup(row_width=2)
donor_add = InlineKeyboardButton(text='Добавить', callback_data="add_donor")
donor_delete = InlineKeyboardButton(text='Удалить', callback_data="delete_donor")
donor_keyboard.add(donor_add, donor_delete)

moder_keyboard = InlineKeyboardMarkup(row_width=2)
moder_add = InlineKeyboardButton(text='Добавить', callback_data="add_moder")
moder_delete = InlineKeyboardButton(text='Удалить', callback_data="delete_moder")
moder_keyboard.add(moder_add, moder_delete)

channel_keyboard = InlineKeyboardMarkup(row_width=2)
channel_add = InlineKeyboardButton(text='Добавить', callback_data="add_channel")
channel_delete = InlineKeyboardButton(text='Удалить', callback_data="delete_channel")
channel_keyboard.add(channel_add, channel_delete)


class Form(StatesGroup):
    name = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    if message.from_user.id == int(USER_ID):
        await bot.send_message(USER_ID, 'Управление базой данных.', reply_markup=keyboard)
    else:
        await bot.send_message(message.from_user.id, 'Недостаточно привелегий для управления!')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')


# Сюда приходит ответ с именем
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await Form.name.set()
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    if check_name == 'donor':
        await bot.send_message(USER_ID,
                               'Выберите действие:', reply_markup=donor_keyboard)

    elif check_name == 'moder':
        await bot.send_message(USER_ID,
                               'Выберите действие:', reply_markup=moder_keyboard)

    elif check_name == 'channel':
        await bot.send_message(USER_ID,
                               'Выберите действие:', reply_markup=channel_keyboard)


@dp.callback_query_handler(state='*')
async def action(call: types.CallbackQuery, state: FSMContext):
    global check_name
    check_name = ''
    if call.data == 'donor':
        await Form.next()
        check_name = call.data
        await bot.send_message(USER_ID, 'Введите название:')

    elif call.data == 'moder':
        await Form.next()
        check_name = call.data
        await bot.send_message(USER_ID, 'Введите название:')

    elif call.data == 'channel':
        await Form.next()
        check_name = call.data
        await bot.send_message(USER_ID, 'Введите название:')

    elif call.data == 'add_donor':
        async with state.proxy() as data:
            await bot.send_message(
                USER_ID, db.add_donor(data['name']))
            await bot.send_message(USER_ID, restart_session.command_execution())

    elif call.data == 'delete_donor':
        async with state.proxy() as data:
            await bot.send_message(
                USER_ID, db.delete_donor(data['name']))
            await bot.send_message(USER_ID, restart_session.command_execution())

    elif call.data == 'add_moder':
        async with state.proxy() as data:
            await bot.send_message(
                USER_ID, db.add_moder(data['name']))
            await bot.send_message(USER_ID, restart_session.command_execution())

    elif call.data == 'delete_moder':
        async with state.proxy() as data:
            await bot.send_message(
                USER_ID, db.delete_moder(data['name']))
            await bot.send_message(USER_ID, restart_session.command_execution())

    elif call.data == 'add_channel':
        async with state.proxy() as data:
            await bot.send_message(
                USER_ID, db.add_channel(data['name']))
            await bot.send_message(USER_ID, restart_session.command_execution())

    elif call.data == 'delete_channel':
        async with state.proxy() as data:
            await bot.send_message(
                USER_ID, db.delete_channel(data['name']))
            await bot.send_message(USER_ID, restart_session.command_execution())

    # await state.finish()


if __name__ == '__main__':
    print(datetime.today().strftime(f'%H:%M:%S | Bot Restart_Telegram launched.'))
    executor.start_polling(dp, skip_updates=True)
