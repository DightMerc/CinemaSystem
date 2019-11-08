import client
from datetime import date, timedelta

def GenerateDescription(movie):
    return f"<b>{movie.title}</b>\n\n<code>{movie.description}</code>\n\n<b>Режиссер:</b> {movie.producer}\n<b>Страна:</b> {movie.country}"
    

def GetAllSessionsDates(movie):
    sessions = client.systemModels.Session.objects.filter(movie=movie)
    days = []
    for session in sessions:
        start = session.startDate
        end = session.endDate

        delta = end - start       # as timedelta

        today = date.today()

        # print(f"\n\n{start}\n\n")
        # print(f"\n\n{end}\n\n")

        for i in range(delta.days + 1):
            day = start + timedelta(days=i)
            if not day < today:
                days.append(day)

        # print(f"\n\n{days}\n\n")
        

    return days