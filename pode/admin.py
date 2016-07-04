from django.contrib import admin

from . import models


class UserCodeAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.UserCode, UserCodeAdmin)
