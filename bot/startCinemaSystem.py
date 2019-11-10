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
import utils

import telegramcalendar
import telegramoptions

from datetime import date, timedelta
import datetime


logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                     level=logging.DEBUG)


bot = Bot(token=client.GetToken(), parse_mode=ParseMode.HTML)
# storage = RedisStorage2(db=9)
dp = Dispatcher(bot, storage=MemoryStorage())

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


@dp.message_handler(state=States.User.MainMenu)
async def process_menu_btns(message: types.Message, state: FSMContext):
    user = message.from_user.id
    recievedText = message.text

    if "кинотеатры" in recievedText.lower():
        await States.User.Cinema.set()

        text = "Выбери кинотеатр"
        await bot.send_message(user, text, reply_markup=keyboards.AllCinemas())
        
    elif "фильмы" in recievedText.lower():
        await States.User.Movie.set()
        
        text = "Выбери фильм"
        await bot.send_message(user, text, reply_markup=keyboards.AllMovies())
        
    elif "помощь" in recievedText.lower():
        await States.User.Help.set()
        
        text = "F.A.Q"
        await bot.send_message(user, text, reply_markup=None)
        
    elif "кэшбэк" in recievedText.lower():
        await States.User.Cashback.set()

        text = "Кэшбэк"
        await bot.send_message(user, text, reply_markup=None)

    
@dp.callback_query_handler(state=States.User.Cinema)
async def process_menu_btns(callback_query: types.CallbackQuery, state: FSMContext):

    user = callback_query.from_user.id
    num = callback_query.data

    


@dp.callback_query_handler(state=States.User.Movie)
async def process_menu_btns(callback_query: types.CallbackQuery, state: FSMContext):

    user = callback_query.from_user.id
    num = callback_query.data

    movie = client.GetMovie(num)
    utils.GetAllSessionsDates(movie)

    text = utils.GenerateDescription(movie)

    async with state.proxy() as data:
        data['movie'] = num 

    await States.User.DateSet.set()


    await bot.send_photo(user, InputFile(os.path.join(client.proj_path, "media", "covers", str(movie.photo.url).replace("media/covers/",""))), caption=text, reply_markup=keyboards.AskDate(movie))


@dp.callback_query_handler(state=States.User.DateSet)
async def process_date(callback_query: types.CallbackQuery, state: FSMContext):

    user = callback_query.from_user.id
    num = int(str(callback_query.data).replace("dateChoose ", ""))

    movie = client.GetMovie(num)

    

    await States.User.ChooseDate.set()

    text = "Выберите наиболее подходящую дату для похода в кино"

    await bot.send_message(user, text, reply_markup=keyboards.FindDate(movie))


@dp.callback_query_handler(state=States.User.ChooseDate)
async def process_date_choose(callback_query: types.CallbackQuery, state: FSMContext):

    user = callback_query.from_user.id

    async with state.proxy() as data:
        num = data['movie']

    movie = client.GetMovie(num)
    query = callback_query

    ret_data = (False,None)
    (action,year,month,day) = telegramcalendar.separate_callback_data(query.data)
    curr = datetime.datetime(int(year), int(month), 1)

    print(f"\n\n{action}\n\n")
    if action == "IGNORE":
        await bot.answer_callback_query(callback_query_id=query.id)
    elif action == "DAY":
        await bot.delete_message(user, query.message.message_id)

        # sessionDay = client.systemModels.SessionMovieDay.objects.filter(date=datetime.date(int(year), int(month), int(day)))
        async with state.proxy() as data:
            data['date'] = datetime.date(int(year), int(month), int(day))
        await States.User.ChooseSession.set()
        text = "Выбери сеанс, который тебе больше по душе"
        await bot.send_message(user, text, reply_markup=keyboards.SessionKeyboard(datetime.date(int(year), int(month), int(day)), num))

    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        await bot.edit_message_text(text=query.message.text,
            chat_id=user,
            message_id=query.message.message_id,
            reply_markup=telegramcalendar.create_calendar(int(pre.year), int(pre.month), utils.GetAllSessionsDates(movie)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        await bot.edit_message_text(text=query.message.text,
            chat_id=user,
            message_id=query.message.message_id,
            reply_markup=telegramcalendar.create_calendar(int(ne.year), int(ne.month), utils.GetAllSessionsDates(movie)))
    else:
        await bot.answer_callback_query(callback_query_id=query.id,text="Something went wrong!")
    return ret_data


@dp.callback_query_handler(state=States.User.ChooseSession)
async def process_session_choose(callback_query: types.CallbackQuery, state: FSMContext):

    user = callback_query.from_user.id

    num = int(callback_query.data)

    await bot.delete_message(user, callback_query.message.message_id)


    async with state.proxy() as data:
        data['session'] = num

    await States.User.TicketNumber.set()

    text = "Выбери количество билетов"
    await bot.send_message(user, text, reply_markup=keyboards.TicketKeyboard())


@dp.callback_query_handler(state=States.User.TicketNumber)
async def process_ticketNumber_choose(callback_query: types.CallbackQuery, state: FSMContext):

    user = callback_query.from_user.id

    num = int(callback_query.data)

    await bot.delete_message(user, callback_query.message.message_id)

    text = ""

    async with state.proxy() as data:
        data['tickets'] = num
        session = data['session']
        date = data['date']

        session = client.systemModels.Session.objects.get(id=session)

        text = utils.GeneratePrecheckout(session, date, num)

        data['date'] = int(session.price * num)
    

    await States.User.TicketNumber.set()
    
    await bot.send_message(user, text, reply_markup=keyboards.BuyKeyboard())




async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    if not os.path.exists(os.getcwd()+"/Users/"):
        os.mkdir(os.getcwd()+"/Users/", 0o777)
        
    executor.start_polling(dp, on_shutdown=shutdown)
