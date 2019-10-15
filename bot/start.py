import logging

from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

import aioredis

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions, InputFile

import keyboards

from typing import Optional
import os

import states as States
import client


logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                     level=logging.DEBUG)


bot = Bot(token=client.GetToken())
storage = RedisStorage2(db=6)
dp = Dispatcher(bot, storage=storage)

dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message, state: FSMContext):
    user = message.from_user.id


    # if not os.path.exists(os.getcwd()+"/Users/" + str(user)):
    #     os.mkdir(os.getcwd()+"/Users/" + str(user), 0o777)

    if not client.IsUserExists(user):
        client.CreateUser(message.from_user)

    await state.set_data({})
    await States.User.JustStarted.set()
    
    await bot.send_chat_action(user, action="typing")

    text = "Привет! Это система для покупки билетов в кинотеатр онлайн. Кайфуй вместе с нами"
    await bot.send_message(user, text)

    text = "Выбери язык"
    await bot.send_message(user, text, reply_markup=keyboards.LanguageKeyboard())
