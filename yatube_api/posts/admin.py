from django.contrib import admin

from posts.models import Post, Group


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text',
                    'pub_date', 'author', 'image')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}
