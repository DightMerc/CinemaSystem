from django.db import models
from django.utils import timezone


class Message(models.Model):
    title = models.CharField(max_length=200)
    number = models.IntegerField(default=0)

    text = models.TextField()

    def __str__(self):
        return "{}) {}".format(self.number, self.title)


class Token(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)
    token = models.CharField("Токен", max_length=255, default="", null=False, blank=False)

    def __str__(self):
        return f"{self.id}: {self.title}"


class PaySystem(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)
    paySystemToken = models.ForeignKey(Token, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.title}"


class Setting(models.Model):
    title = models.CharField("Название", max_length=255, default="", null=False, blank=False)
    telegramBotToken = models.ForeignKey(Token, on_delete=models.CASCADE)
    active = models.BooleanField("Активно", default=False)

    paySystem = models.ManyToManyField(PaySystem)

    def __str__(self):
        return f"{self.id}: {self.title}"


class TelegramUser(models.Model):
    telegramId = models.PositiveIntegerField("Telegram ID")

    fullName = models.CharField("Полное имя", max_length=255, default="", null=False, blank=False)
    username = models.CharField("Username", max_length=255, default="", null=True)
    phone = models.PositiveIntegerField("Номер телефона", null=True, blank=True)

    language = models.CharField("Язык", max_length=5, default="RU")

    registrationDate = models.DateTimeField("Дата регистрации", default=timezone.now)

    def __str__(self):
        return f"{self.id}: {self.telegramId}"
