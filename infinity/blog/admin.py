from django.contrib import admin
from .models import Post

from django_summernote.admin import SummernoteModelAdmin



class PostAdmin(SummernoteModelAdmin):
    # list_display = ('title', 'slug', 'status','created_on')
    # list_filter = ("status",)
    # search_fields = ['title', 'content']
    # prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


class PostEditAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)
