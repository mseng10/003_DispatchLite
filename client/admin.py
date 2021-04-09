from django.contrib import admin
from .models import Client, Template

class ClientAdmin(admin.ModelAdmin):
    pass

admin.site.register(Client, ClientAdmin)

class TemplatesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Template, TemplatesAdmin)
