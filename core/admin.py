from django.contrib import admin
from .models import Profile, Picturegram, PostLikes, Follow

# Register your models here.
admin.site.register(Profile)
admin.site.register(Picturegram)
admin.site.register(PostLikes)
admin.site.register(Follow)