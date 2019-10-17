import os
import sys

import django
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import shutil
# from django.conf import settings


proj_path = os.path.join(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0], "bothelper")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bothelper.settings")
sys.path.append(proj_path)

print(proj_path)
django.setup()

from bot import models as botModels
from system import models as systemModels


def GetToken():
    return botModels.Setting.objects.get(active=True).telegramBotToken.token


def IsUserExists(user):

    try:
        botModels.TelegramUser.objects.get(telegramId=int(user))
        return True
    except Exception as e:
        return False


def CreateUser(user):

    newUser = botModels.TelegramUser()
    newUser.telegramId = int(user.id)
    newUser.fullName = str(user.full_name)
    newUser.username = str(user.username)

    newUser.save()

    return newUser


def getMessage(number):
    return botModels.Message.objects.get(number=int(number)).text


def SetUserLanguage(user, language):
    
    current_user = botModels.TelegramUser.objects.get(telegramId=int(user))
    current_user.language = language

    current_user.save()

    return language


def GetAllCinemas():

    return systemModels.Cinema.objects.filter(active=True)


def GetAllMovies():

    return systemModels.Movie.objects.filter(active=True)


def GetMovie(id):

    return systemModels.Movie.objects.get(id=id)


if __name__ == "__main__":
    pass
