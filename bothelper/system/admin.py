from django.contrib import admin

from .models import Staff, StaffPosition
from .models import Movie, Session, SessionMovieDay, Cinema, Ticket


# Register your models here.


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'active', 'registrationDate')
    ordering = ('id',)
    search_fields = ('id', 'StaffPosition', 'fullName')


@admin.register(StaffPosition)
class StaffPositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'active', 'producer', 'yearOfIssue', 'country')
    ordering = ('id',)
    search_fields = ('id', 'title', 'producer', 'country')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'active', 'startDate', 'endDate', 'price')
    ordering = ('id',)
    search_fields = ('id', 'title', 'movie', 'country')


@admin.register(SessionMovieDay)
class SessionMovieDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'used', 'user', 'cinema', 'session', 'price', 'hash')
    ordering = ('id',)
    search_fields = ('id', 'used', 'user', 'cinema', 'session', 'price', 'hash')
