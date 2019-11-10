import client
from datetime import date, timedelta

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


def GeneratePrecheckout(session, date, count):
    movies = ""
    for movie in session.movie.all():
        movies += f" + {movie.title}"

    price = int(session.price * count)
    return f"<b>{movies}</b>\n\n<b>Кинотеатр:</b> {session.cinema.title}\n\n<b>Общая цена:</b> {price} сум"
