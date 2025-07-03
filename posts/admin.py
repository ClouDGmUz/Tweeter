from django.contrib import admin
from .models import Post, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin interface for Post model
    """
    list_display = ('display_author', 'content_preview', 'is_reply', 'like_count_display', 'reply_count_display', 'created_at')
    list_filter = ('created_at', 'author_name', 'parent_post')
    search_fields = ('content', 'author_name')
    readonly_fields = ('created_at', 'updated_at', 'like_count_display', 'reply_count_display')
    ordering = ('-created_at',)
    raw_id_fields = ('parent_post',)
    
    def content_preview(self, obj):
        """Show a preview of the post content"""
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def like_count_display(self, obj):
        """Display like count"""
        return obj.get_like_count()
    like_count_display.short_description = 'Likes'
    
    def reply_count_display(self, obj):
        """Display reply count"""
        return obj.get_reply_count()
    reply_count_display.short_description = 'Replies'
    
    def is_reply(self, obj):
        """Show if post is a reply"""
        return obj.is_reply
    is_reply.boolean = True
    is_reply.short_description = 'Is Reply'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """
    Admin interface for Like model
    """
    list_display = ('post_preview', 'author_name', 'session_key', 'created_at')
    list_filter = ('created_at', 'author_name')
    search_fields = ('post__content', 'author_name', 'session_key')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    raw_id_fields = ('post',)
    
    def post_preview(self, obj):
        """Show a preview of the liked post"""
        return obj.post.content[:50] + '...' if len(obj.post.content) > 50 else obj.post.content
    post_preview.short_description = 'Post'
