from django.contrib import admin

from .models import Token, TelegramUser, Setting, PaySystem, Message


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'token')
    ordering = ('id',)
    search_fields = ('id', 'title', 'token')


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegramId', 'fullName', 'username', 'phone', 'language', 'registrationDate')
    ordering = ('id',)
    search_fields = ('id', 'telegramId', 'fullName', 'username', 'phone', 'language', 'registrationDate')


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'telegramBotToken', 'active')
    ordering = ('id',)
    search_fields = ('id', 'title', 'telegramBotToken', 'active')


@admin.register(PaySystem)
class PaySystemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'paySystemToken')
    ordering = ('id',)
    search_fields = ('id', 'title', 'paySystemToken')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'text')
    ordering = ('number',)
    search_fields = ('number', 'title', 'text')
