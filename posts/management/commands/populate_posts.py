from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from posts.models import Post, Like


class Command(BaseCommand):
    help = 'Populate the database with sample posts, replies, and likes'

    def handle(self, *args, **options):
        # Clear existing data
        Like.objects.all().delete()
        Post.objects.all().delete()
        self.stdout.write('Cleared existing posts and likes.')

        # Sample post data
        sample_posts = [
            {
                'content': 'Just discovered this amazing new coffee shop downtown! ☕ The atmosphere is perfect for working.',
                'author_name': 'Sarah Johnson'
            },
            {
                'content': 'Beautiful sunset today! Sometimes you just need to stop and appreciate the simple things in life. 🌅',
                'author_name': 'Mike Chen'
            },
            {
                'content': 'Working on a new Django project and loving how clean the code structure is. Python really is elegant! 🐍',
                'author_name': 'Alex Rodriguez'
            },
            {
                'content': 'Anyone else excited for the weekend? Planning to go hiking and disconnect from technology for a bit.',
                'author_name': None  # Anonymous post
            },
            {
                'content': 'Just finished reading an incredible book about artificial intelligence. The future is fascinating! 🤖',
                'author_name': 'Emma Thompson'
            },
            {
                'content': 'Cooking experiment: homemade pasta from scratch. It\'s messier than expected but so worth it! 🍝',
                'author_name': 'David Kim'
            },
            {
                'content': 'Rainy day = perfect excuse to stay in and binge-watch that series everyone\'s been talking about. 🌧️',
                'author_name': None  # Anonymous post
            },
            {
                'content': 'Morning run completed! There\'s something magical about the city waking up. Ready to tackle the day! 🏃‍♀️',
                'author_name': 'Lisa Park'
            }
        ]

        # Sample replies
        sample_replies = [
            {
                'content': 'Which coffee shop? I\'m always looking for new places to work from!',
                'author_name': 'Tom Wilson',
                'parent_index': 0  # Reply to first post
            },
            {
                'content': 'I love that place! Their espresso is incredible.',
                'author_name': None,
                'parent_index': 0  # Another reply to first post
            },
            {
                'content': 'Django is amazing! What kind of project are you building?',
                'author_name': 'Jessica Lee',
                'parent_index': 2  # Reply to Django post
            },
            {
                'content': 'Hiking sounds perfect! Where are you planning to go?',
                'author_name': 'Mark Davis',
                'parent_index': 3  # Reply to hiking post
            },
            {
                'content': 'What book was it? I\'m always looking for good AI reads.',
                'author_name': 'Rachel Green',
                'parent_index': 4  # Reply to AI book post
            }
        ]

        # Create main posts with varied timestamps
        created_posts = []
        for i, post_data in enumerate(sample_posts):
            # Create posts with timestamps spread over the last few days
            created_time = timezone.now() - timedelta(
                days=random.randint(0, 3),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            post = Post.objects.create(
                content=post_data['content'],
                author_name=post_data['author_name'],
                created_at=created_time
            )
            created_posts.append(post)
            
        # Create replies
        for reply_data in sample_replies:
            parent_post = created_posts[reply_data['parent_index']]
            reply_time = parent_post.created_at + timedelta(
                hours=random.randint(1, 12),
                minutes=random.randint(0, 59)
            )
            
            Post.objects.create(
                content=reply_data['content'],
                author_name=reply_data['author_name'],
                parent_post=parent_post,
                created_at=reply_time
            )

        # Create sample likes
        sample_users = ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson', None, None]
        
        for post in created_posts:
            # Randomly like posts
            num_likes = random.randint(0, 5)
            liked_users = random.sample(sample_users, min(num_likes, len(sample_users)))
            
            for user in liked_users:
                # Generate a fake session key for anonymous users
                session_key = f'session_{random.randint(1000, 9999)}' if user is None else None
                
                Like.objects.create(
                    post=post,
                    author_name=user,
                    session_key=session_key
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(sample_posts)} posts, {len(sample_replies)} replies, and sample likes!')
        )