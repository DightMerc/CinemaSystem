from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import client

import telegramcalendar
import telegramoptions
import utils


def AskDate(movie):
    return InlineKeyboardMarkup().add(InlineKeyboardButton('Выбрать дату', callback_data=f'dateChoose {movie.id}'))


def FindDate(movie):
    return telegramcalendar.create_calendar(days=utils.GetAllSessionsDates(movie))


def SessionKeyboard(date, movie):
    currentMovie = client.systemModels.Movie.objects.get(id=movie)
    sessionDays = client.systemModels.SessionMovieDay.objects.filter(date=date)
    sessions = []
    for sessionDay in sessionDays:
        session = sessionDay.session
        if currentMovie in session.movie.all():
            sessions.append(session)

    button_list = []

    cinemas = client.GetAllCinemas()

    for session in sessions:
        movies = ""
        for movie in session.movie.all():
            movies += f" + {movie.title}"
        button_list.append(InlineKeyboardButton(f'{movies}: {session.cinema.title}', callback_data=f'{session.id}'))
    footer = []

    footer.append(InlineKeyboardButton('⏮ Назад', callback_data='back'))
    return InlineKeyboardMarkup(inline_keyboard=buildMenu(button_list, n_cols=2, footer_buttons=footer))

# def SessionPaginatoinKeyboard(length, current, user):
#     keyboard = InlineKeyboardMarkup()
#         if current!=1:
#             if current==length:
#                 keyboard.row(
#                         InlineKeyboardButton(text="<<", callback_data="pagination prev {}".format(current-1)),
#                         InlineKeyboardButton(text="{}/{}".format(current, length), callback_data="pagination None"),
#                         InlineKeyboardButton(text=">>", callback_data="pagination next {}".format(current+1)))
#             else:
#                 keyboard.row(
#                         InlineKeyboardButton(text="<<", callback_data="pagination prev {}".format(current-1)),
#                         InlineKeyboardButton(text="{}/{}".format(current, length), callback_data="pagination None"),
#                         InlineKeyboardButton(text=">>", callback_data="pagination next {}".format(current+1)))
#         else:
#             keyboard.row(
#                     InlineKeyboardButton(text="<<", callback_data="pagination prev {}".format(current-1)),
#                     InlineKeyboardButton(text="{}/{}".format(current, length), callback_data="pagination None"),
#                     InlineKeyboardButton(text=">>", callback_data="pagination next {}".format(current+1)))

#         # if client.getUserLanguage(user)=="RU":
#             keyboard.row(InlineKeyboardButton(text="Изменить", callback_data="pagination change {}".format(current)),
#                     InlineKeyboardButton(text="Удалить", callback_data="pagination delete {}".format(current)))
#             keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="pagination cancel"))
#         # else:
#         #         keyboard.row(InlineKeyboardButton(text="Ўзгартириш", callback_data="pagination change {}".format(current)),
#         #                 InlineKeyboardButton(text="Удалить", callback_data="pagination delete {}".format(current)))
#         #         keyboard.add(InlineKeyboardButton(text="Бекор килиш", callback_data="pagination cancel"))

#         return keyboard


def BuyKeyboard():
    return InlineKeyboardMarkup().add(InlineKeyboardButton('Оплатить', callback_data=f'pay')
    ).add(InlineKeyboardButton('⏮ Назад', callback_data='back'))


def PaySystemkeyboard(systems):
    button_list = []

    for system in systems:
        button_list.append(InlineKeyboardButton(f'{system.title}', callback_data=f'{system.id}'))
    footer = []

    footer.append(InlineKeyboardButton('⏮ Назад', callback_data='back'))
    return InlineKeyboardMarkup(inline_keyboard=buildMenu(button_list, n_cols=2, footer_buttons=footer))


def TicketKeyboard():
    button_list = []

    cinemas = client.GetAllCinemas()

    for a in range(1, 11):
        button_list.append(InlineKeyboardButton(f'{a}', callback_data=f'{a}'))
    footer = []

    footer.append(InlineKeyboardButton('⏮ Назад', callback_data='back'))
    return InlineKeyboardMarkup(inline_keyboard=buildMenu(button_list, n_cols=2, footer_buttons=footer))


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
