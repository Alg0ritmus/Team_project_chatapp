from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Chat_user)
admin.site.register(Chat_room)
admin.site.register(Chat_msg)


