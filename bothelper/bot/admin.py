from django.contrib import admin
from .models import Token, PaySystem, Setting

# Register your models here.


admin.site.register(Token)
admin.site.register(PaySystem)
admin.site.register(Setting)
