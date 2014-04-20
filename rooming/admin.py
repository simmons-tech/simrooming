from django.contrib import admin
from rooming.models import Room, GRT, Resident

admin.site.register(GRT)
admin.site.register(Resident)

from django.contrib import admin

class AuthorAdmin(admin.ModelAdmin):
    list_per_page = 1000
admin.site.register(Room, AuthorAdmin)
