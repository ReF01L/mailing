from django.contrib import admin

from .models import Mailing, Client, Message


class ClientAdmin(admin.ModelAdmin):
    list_display = ("number", "mobile_code", "tag", "timezone")


admin.site.register(Mailing)
admin.site.register(Client, ClientAdmin)
admin.site.register(Message)
