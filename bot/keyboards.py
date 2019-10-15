from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import client


def LanguageKeyboard():

    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
        KeyboardButton('Ўзбек тили'),
        KeyboardButton('Русский язык')
)


def MainMenuKeyboard(user):

    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
                KeyboardButton('Сеансы'),
                KeyboardButton('Кинотеатры')
        ).add(KeyboardButton("Кэшбэк")
        ).add(KeyboardButton("Помощь"))
