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
                KeyboardButton('Фильмы'),
                KeyboardButton('Кинотеатры')
        ).add(KeyboardButton("Кэшбэк")
        ).add(KeyboardButton("Помощь"))


def AllCinemas():
    button_list = []

    cinemas = client.GetAllCinemas()

    for cinema in cinemas:
        button_list.append(InlineKeyboardButton(f'{cinema.title}', callback_data=f'{cinema.id}'))
    footer = []

    footer.append(InlineKeyboardButton('⏮ Назад',callback_data='back'))
    return InlineKeyboardMarkup(inline_keyboard=buildMenu(button_list, n_cols=2, footer_buttons=footer))


def AllMovies():
    button_list = []

    movies = client.GetAllMovies()

    for movie in movies:
        button_list.append(InlineKeyboardButton(f'{movie.title}', callback_data=f'{movie.id}'))
    footer = []

    footer.append(InlineKeyboardButton('⏮ Назад',callback_data='back'))
    return InlineKeyboardMarkup(inline_keyboard=buildMenu(button_list, n_cols=2, footer_buttons=footer))


def buildMenu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        for btn in footer_buttons:
            menu.append([btn])
    return menu
