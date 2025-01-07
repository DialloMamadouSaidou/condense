from django.contrib import admin

from .models import MyUser, Profile


@admin.register(MyUser)
class MyUser(admin.ModelAdmin):
    list_display = (
        'email',
        'name'
    )

@admin.register(Profile)
class MyProfile(admin.ModelAdmin):
    list_display = (
        'user',
        'choices'
    )