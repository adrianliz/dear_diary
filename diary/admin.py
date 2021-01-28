from django.contrib import admin

from .models import Mood, Profile, ContactMessage, Advice

admin.site.register(Mood)
admin.site.register(Profile)
admin.site.register(ContactMessage)
admin.site.register(Advice)
