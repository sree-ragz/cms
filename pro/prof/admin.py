from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Participant)
admin.site.register(PaperSubmition)
admin.site.register(Privillage)
admin.site.register(PosterSubmition)
admin.site.register(Event)
admin.site.register(User_Event)
admin.site.register(Reviewer_Paper)
admin.site.register(Reviewer_Poster)
admin.site.register(ParticipantType)
admin.site.register(ContextSubmition)
admin.site.register(Reviewer_Context)