from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Post, Like
import json


class PostListView(ListView):
    """
    View to display all posts in chronological order (newest first)
    """
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20  # Show 20 posts per page
    
    def get_queryset(self):
        """Get posts with like and reply counts, excluding replies from main feed"""
        queryset = Post.objects.filter(parent_post__isnull=True).annotate(
            like_count=Count('likes'),
            reply_count=Count('replies')
        ).order_by('-created_at')
        
        # Handle search
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(content__icontains=search_query) | 
                Q(author_name__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add additional context data"""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        
        # Add session key for like checking
        if not self.request.session.session_key:
            self.request.session.create()
        context['session_key'] = self.request.session.session_key
        
        return context


class TrendingPostsView(ListView):
    """
    View to display trending posts (most liked posts)
    """
    model = Post
    template_name = 'posts/trending.html'
    context_object_name = 'posts'
    paginate_by = 20
    
    def get_queryset(self):
        """Get posts ordered by like count"""
        return Post.objects.filter(parent_post__isnull=True).annotate(
            like_count=Count('likes'),
            reply_count=Count('replies')
        ).order_by('-like_count', '-created_at')


class PostDetailView(View):
    """
    View to display a single post with its replies
    """
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        replies = Post.objects.filter(parent_post=post).annotate(
            like_count=Count('likes'),
            reply_count=Count('replies')
        ).order_by('created_at')
        
        # Ensure session exists
        if not request.session.session_key:
            request.session.create()
        
        context = {
            'post': post,
            'replies': replies,
            'session_key': request.session.session_key
        }
        return render(request, 'posts/post_detail.html', context)


class CreatePostView(View):
    """
    View to handle post creation and replies
    """
    def post(self, request):
        content = request.POST.get('content', '').strip()
        author_name = request.POST.get('author_name', '').strip()
        parent_post_id = request.POST.get('parent_post_id')
        
        # Validate content
        if not content:
            messages.error(request, 'Post content cannot be empty.')
            return self._redirect_back(request, parent_post_id)
        
        if len(content) > 280:
            messages.error(request, 'Post content cannot exceed 280 characters.')
            return self._redirect_back(request, parent_post_id)
        
        # Get parent post if this is a reply
        parent_post = None
        if parent_post_id:
            try:
                parent_post = Post.objects.get(id=parent_post_id)
            except Post.DoesNotExist:
                messages.error(request, 'Parent post not found.')
                return redirect('post_list')
        
        # Create the post
        Post.objects.create(
            content=content,
            author_name=author_name if author_name else None,
            parent_post=parent_post
        )
        
        success_msg = 'Reply posted successfully!' if parent_post else 'Post created successfully!'
        messages.success(request, success_msg)
        return self._redirect_back(request, parent_post_id)
    
    def _redirect_back(self, request, parent_post_id):
        """Helper method to redirect back to appropriate page"""
        if parent_post_id:
            return redirect('post_detail', post_id=parent_post_id)
        return redirect('post_list')


class LikePostView(View):
    """
    View to handle post likes/unlikes via AJAX
    """
    def post(self, request):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Invalid request'}, status=400)
        
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')
            author_name = data.get('author_name', '').strip()
            
            post = get_object_or_404(Post, id=post_id)
            
            # Ensure session exists
            if not request.session.session_key:
                request.session.create()
            
            session_key = request.session.session_key
            
            # Check if already liked
            like, created = Like.objects.get_or_create(
                post=post,
                session_key=session_key,
                defaults={'author_name': author_name if author_name else None}
            )
            
            if not created:
                # Unlike the post
                like.delete()
                liked = False
            else:
                liked = True
            
            return JsonResponse({
                'liked': liked,
                'like_count': post.get_like_count()
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def home_view(request):
    """
    Home view that redirects to post list
    """
    return redirect('post_list')
