from django.contrib import admin
from chat import models

admin.site.register(models.Post)
admin.site.register(models.UserGroup)
admin.site.register(models.Group)
