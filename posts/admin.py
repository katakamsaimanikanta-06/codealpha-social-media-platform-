from django.contrib import admin
from .models import Post, Like, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content_snippet', 'likes_count', 'comments_count', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)
    inlines = [CommentInline]

    def content_snippet(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'created_at')
    search_fields = ('author__username', 'content')
