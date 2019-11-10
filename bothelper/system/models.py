from django.db import models
from django.utils import timezone
from bot.models import Token, TelegramUser, PaySystem

from datetime import date, timedelta



# Create your models here.


class Movie(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)
    active = models.BooleanField("Активно", default=False)

    photo = models.ImageField("Фото", upload_to="media/covers")

    description = models.TextField("Описание")
    
    producer = models.CharField("Режиссер", max_length=255, default="", null=True, blank=True)

    yearOfIssue = models.DateField("Дата выпуска в показ")
    country = models.CharField("Страна", max_length=255, default="", null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.title}"


class Cinema(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)
    active = models.BooleanField("Активно", default=False)

    def __str__(self):
        return f"{self.id}: {self.title}"


class StaffPosition(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)

    def __str__(self):
        return f"{self.id}: {self.title}"


class Session(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)
    active = models.BooleanField("Активно", default=False)

    movie = models.ManyToManyField(Movie)

    price = models.PositiveIntegerField("Цена")
    time = models.TimeField("Время начала сеанса")

    duration = models.CharField("Длительность", max_length=255, default="", null=False, blank=False)

    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    startDate = models.DateField("Дата начала показа сеанса")
    endDate = models.DateField("Дата окончания показа сеанса")

    def __str__(self):
        return f"{self.id}: {self.title}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)  # Call the "real" save() method.

        start = self.startDate
        end = self.endDate

        delta = end - start       # as timedelta

        today = date.today()

        for i in range(delta.days + 1):
            
            day = start + timedelta(days=i)
            sessionDay = SessionMovieDay()
            sessionDay.title = f"{self.title}: {day}"
            sessionDay.date = day
            sessionDay.tickets = 35
            sessionDay.session = self
            sessionDay.save()


class Ticket(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)

    buyDate = models.DateTimeField("Дата приобретения билета", default=timezone.now, null=False, blank=False)
    applyDate = models.DateTimeField("Дата использования билета", null=True, blank=True)

    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    price = models.PositiveIntegerField("Цена", default=0, null=False, blank=False)

    def __str__(self):
        return f"{self.id}: {self.session}"


class Staff(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)

    active = models.BooleanField("Активно", default=False)

    position = models.ForeignKey(StaffPosition, on_delete=models.CASCADE)

    fullName = models.CharField("Полное имя", max_length=255, default="", null=False, blank=False)
    appliedTickets = models.ManyToManyField(Ticket)

    registrationDate = models.DateTimeField("Дата регистрации", default=timezone.now)

    def __str__(self):
        return f"{self.id}: {self.title}"


class SessionMovieDay(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)
    date = models.DateField("День", null=False, blank=False)

    tickets = models.PositiveIntegerField("Количество билетов", default=35, null=False, blank=False)

    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}: {self.date}"