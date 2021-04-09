from django.contrib import admin
from .models import Client, Template, Campaign, Population

class ClientAdmin(admin.ModelAdmin):
    pass

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