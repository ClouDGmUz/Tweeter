# Fun - Twitter-like Social Media App

A Twitter-like social media web application built with Django that allows users to post tweets, like posts, reply to others, and discover trending content.

## Features

- Post tweets with your name or anonymously (up to 280 characters)
- Like/unlike posts with real-time updates
- Reply to posts with threaded conversations
- Search posts by content or author name
- View trending posts (sorted by popularity)
- Responsive web interface with modern UI
- Session-based interactions (no registration required)
- Pagination for better performance

## Tech Stack

- Django (Web Framework)
- SQLite database
- HTML/CSS/JavaScript (Frontend)
- Bootstrap-inspired styling
- AJAX for dynamic interactions
- Python

## Web Pages

- `/` - Home page (redirects to post list)
- `/posts/` - Main feed with all posts
- `/posts/trending/` - Trending posts by popularity
- `/posts/post/<id>/` - Individual post detail with replies
- `/posts/create/` - Create new posts (POST only)
- `/posts/like/` - Like/unlike posts (AJAX endpoint)

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. (Optional) Populate sample data: `python manage.py populate_posts`
7. Start server: `python manage.py runserver`
8. Open your browser and navigate to `http://127.0.0.1:8000/`

## Usage

### Web Interface
- **Create Posts**: Use the form at the top of the main page to create new posts
- **Like Posts**: Click the heart icon to like/unlike posts
- **Reply to Posts**: Click "Reply" on any post to view details and add replies
- **Search**: Use the search bar to find posts by content or author
- **Trending**: Visit `/posts/trending/` to see the most popular posts

### Management Commands
- `python manage.py populate_posts` - Creates sample posts, replies, and likes for testing
