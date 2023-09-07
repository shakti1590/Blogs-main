from django.contrib import admin
from General.models import *

admin.site.site_header = 'Blogs Admin Panel'
admin.site.index_title = 'Welcome!'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'email', 'phone', 'message')

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'email', 'phone', 'category', 'topic', 'approved')    

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display=('id', 'email') 

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=('id', 'title', 'category', 'user', 'date', 'featured_image', 'approved', 'featured')
