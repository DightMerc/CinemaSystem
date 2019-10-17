from django.db import models
from django.utils import timezone
from bot.models import Token, TelegramUser, PaySystem


# Create your models here.


class Movie(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)
    active = models.BooleanField("Активно", default=False)

    description = models.TextField("Описание")
    
    producer = models.CharField("Режиссер", max_length=255, default="", null=True, blank=True)

    yearOfIssue = models.DateField("Дата выпуска в показ")
    country = models.CharField("Страна", max_length=255, default="", null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.title}"


class Session(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)
    active = models.BooleanField("Активно", default=False)

    movie = models.ManyToManyField(Movie)

    price = models.PositiveIntegerField("Цена")
    time = models.TimeField("Время начала сеанса")

    duration = models.TimeField("Длительность")

    startDate = models.DateField("Дата начала показа сеанса")
    endDate = models.DateField("Дата окончания показа сеанса")

    def __str__(self):
        return f"{self.id}: {self.title}"


class SessionDay(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)
    date = models.DateField("День", null=False, blank=False)

    sessions = models.ManyToManyField(Session)

    def __str__(self):
        return f"{self.title}: {self.date}"


class Cinema(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)
    active = models.BooleanField("Активно", default=False)

    def __str__(self):
        return f"{self.id}: {self.title}"


class Ticket(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)

    buyDate = models.DateTimeField("Дата приобретения билета", default=timezone.now, null=False, blank=False)
    applyDate = models.DateTimeField("Дата использования билета", null=True, blank=True)

    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    price = models.PositiveIntegerField("Цена", default=0, null=False, blank=False)

    def __str__(self):
        return f"{self.id}: {self.session}"


class StaffPosition(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)

    def __str__(self):
        return f"{self.id}: {self.title}"


class Staff(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)

    active = models.BooleanField("Активно", default=False)

    position = models.ForeignKey(StaffPosition, on_delete=models.CASCADE)

    fullName = models.CharField("Полное имя", max_length=255, default="", null=False, blank=False)
    appliedTickets = models.ManyToManyField(Ticket)

    registrationDate = models.DateTimeField("Дата регистрации", default=timezone.now)

    def __str__(self):
        return f"{self.id}: {self.title}"