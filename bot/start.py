import logging

from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

import aioredis

from aiogram.dispatcher import FSMContext

from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions, InputFile

import keyboards

from typing import Optional
import os

import states as States
import client


logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                     level=logging.DEBUG)


bot = Bot(token=client.GetToken())
storage = RedisStorage2(db=9)
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


@dp.message_handler(state=States.User.JustStarted)
async def process_start_command(message: types.Message, state: FSMContext):
    user = message.from_user.id
    recievedText = message.text

    if "ру" in recievedText.lower():
        client.SetUserLanguage(user, "ru")
    elif "bek" in recievedText.lower():
        client.SetUserLanguage(user, "uz")

    text = "Отлично!"
    await bot.send_message(user, text)

    await States.User.MainMenu.set()
    text = "Отлично! Теперь выбери действие"
    await bot.send_message(user, text, reply_markup=keyboards.MainMenuKeyboard(user))


@dp.message_handler(state=States.User.CinemaSet)
async def process_start_command(message: types.Message, state: FSMContext):
    user = message.from_user.id
    recievedText = message.text

    if "ру" in recievedText.lower():
        client.SetUserLanguage(user, "ru")
    elif "bek" in recievedText.lower():
        client.SetUserLanguage(user, "uz")

    text = "Отлично!"
    await bot.send_message(user, text)

    await States.User.MainMenu.set()
    text = "Отлично! Теперь выбери действие"
    await bot.send_message(user, text, reply_markup=keyboards.MainMenuKeyboard(user))


@dp.message_handler(state=States.User.MainMenu)
async def process_menu_btns(message: types.Message, state: FSMContext):
    user = message.from_user.id
    recievedText = message.text

    if "кинотеатры" in recievedText.lower():
        await States.User.Cinema.set()

        text = ""
        await bot.send_message(user, text, reply_markup=None)
        
    elif "сеансы" in recievedText.lower():
        await States.User.Session.set()
        
        text = ""
        await bot.send_message(user, text, reply_markup=None)
        
    elif "помощь" in recievedText.lower():
        await States.User.Help.set()
        
        text = ""
        await bot.send_message(user, text, reply_markup=None)
        
    elif "кэшбэк" in recievedText.lower():
        await States.User.Cashback.set()

        text = ""
        await bot.send_message(user, text, reply_markup=None)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    if not os.path.exists(os.getcwd()+"/Users/"):
        os.mkdir(os.getcwd()+"/Users/", 0o777)
        
    executor.start_polling(dp, on_shutdown=shutdown)
