import client
from datetime import date, timedelta
import hashlib
import pyqrcode
import os

def GenerateDescription(movie):
    return f"<b>{movie.title}</b>\n\n<code>{movie.description}</code>\n\n<b>Режиссер:</b> {movie.producer}\n<b>Страна:</b> {movie.country}"
    

def GetAllSessionsDates(movie):
    sessions = client.systemModels.Session.objects.filter(movie=movie)
    days = []
    for session in sessions:
        currentDayMovieSession = client.systemModels.SessionMovieDay.objects.filter(session=session)

        start = session.startDate
        end = session.endDate

        delta = end - start       # as timedelta

        today = date.today()

        for i in range(delta.days + 1):
            
            day = start + timedelta(days=i)
            if not day < today:
                try:
                    if currentDayMovieSession.get(date=day).tickets > 0:
                        days.append(day)
                except Exception as e:
                    pass

    return days


def GenerateTicket(user, session_num, now, price, hash):
    client.CreateTicket(user, session_num, now, price, hash)
    return


def GenerateTicketHASH(user, date, session_num, now):
    textToHASH = f"{user} {date} {session_num} {now}"
    return str(hashlib.md5(str.encode(textToHASH)).hexdigest())

def qrGenerate(hash):
    img = pyqrcode.create(hash)
    img.png(os.path.join(os.getcwd(), "codes", f"{hash}.png"), scale=8)

    return os.path.join(os.getcwd(), "codes", f"{hash}.png")




def GeneratePrecheckout(session, date, count):
    movies = ""
    for movie in session.movie.all():
        if movies == "":
            movies += f"{movie.title}"
        else:
            movies += f" + {movie.title}"

    price = int(session.price * count)
    return f"<b>{str(session.time)[:5]} {movies}</b>\n\n<b>Кинотеатр:</b> {session.cinema.title}\n\n<b>Общая цена:</b> {price} сум"
