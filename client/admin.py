from django.contrib import admin
from .models import Client, Template, Campaign, Population, Batch, Message


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'key')

admin.site.register(Client, ClientAdmin)

class TemplatesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Template, TemplatesAdmin)

class CampaignAdmin(admin.ModelAdmin):
    pass

admin.site.register(Campaign, CampaignAdmin)

class PopulationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Population, PopulationAdmin)

class BatchAdmin(admin.ModelAdmin):
    pass

admin.site.register(Batch, BatchAdmin)

class MessageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Message, MessageAdmin)
