from django.contrib.auth.models import User
from django.contrib import admin
from blogengine.models import Post,UserProfile
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("title",)}

admin.site.register(UserProfile)
admin.site.register(Post,PostAdmin)