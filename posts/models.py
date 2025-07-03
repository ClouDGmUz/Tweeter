from django.db import models
from django.utils import timezone
from django.db.models import Count


class Post(models.Model):
    """
    Model representing a Twitter-like post with optional author name
    """
    content = models.TextField(max_length=280, help_text="Post content (max 280 characters)")
    author_name = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="Optional author name"
    )
    parent_post = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies',
        help_text="Parent post if this is a reply"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # Show newest posts first
        
    def __str__(self):
        author = self.author_name or "Anonymous"
        post_type = "Reply" if self.parent_post else "Post"
        return f"{post_type} by {author}: {self.content[:50]}..."
    
    @property
    def display_author(self):
        """Return author name or 'Anonymous' if no name provided"""
        return self.author_name or "Anonymous"
    
    @property
    def is_reply(self):
        """Check if this post is a reply to another post"""
        return self.parent_post is not None
    
    def get_like_count(self):
        """Get the number of likes for this post"""
        return self.likes.count()
    
    def get_reply_count(self):
        """Get the number of replies for this post"""
        return self.replies.count()
    
    def is_liked_by_session(self, session_key):
        """Check if this post is liked by the current session"""
        return self.likes.filter(session_key=session_key).exists()


class Like(models.Model):
    """
    Model representing a like on a post
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    session_key = models.CharField(max_length=40, blank=True, null=True, help_text="Session key for anonymous users")
    author_name = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="Optional name of the person who liked"
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('post', 'session_key')  # Prevent duplicate likes from same session
        ordering = ['-created_at']
    
    def __str__(self):
        author = self.author_name or "Anonymous"
        return f"{author} liked: {self.post.content[:30]}..."
