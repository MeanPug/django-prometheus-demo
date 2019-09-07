from django.contrib import admin
from walker import models


class WalkerAdmin(admin.ModelAdmin):
    fields = ['name', 'email']


class DogAdmin(admin.ModelAdmin):
    fields = ['size', 'name', 'age']


admin.site.register(models.Walker, WalkerAdmin)
admin.site.register(models.Dog, DogAdmin)
