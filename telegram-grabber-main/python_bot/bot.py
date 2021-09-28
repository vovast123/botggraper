import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import os
import sys
from sqll.sql import SQL
base_dir = os.path.abspath(os.path.join(os.path.dirname('bot_grabber.py'), '..'))
sys.path.append(base_dir)

chat_id = "redqwaszx"# id канала 
ch_id = 'redqwaszxred'
donor = 'rrrrrrrrrreeeeeeeee'
api_id ='8672592'
api_hash = '1a79bf2aa03dd76d22e86aee7fd1e524'
bd = SQL('../bd.db')


