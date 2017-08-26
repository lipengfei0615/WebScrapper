from django.contrib import admin

from .models import Athletes,Matchinfo,Meet,ParticipatingNation,Personalbest,Ranking,Recordlist,Records
# Register your models here.
admin.site.register(Athletes)
admin.site.register(Matchinfo)
admin.site.register(Meet)
admin.site.register(ParticipatingNation)
admin.site.register(Personalbest)
admin.site.register(Ranking)
admin.site.register(Recordlist)
admin.site.register(Records)