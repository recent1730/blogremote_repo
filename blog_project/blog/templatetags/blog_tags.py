from blog.models import Post
from django import template
from django.db.models import Count

register=template.Library()

@register.simple_tag()
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('blog/latest_posts123.html')
def show_latest_posts(count=3):
    latest_posts=Post.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.inclusion_tag('blog/comment_posts123.html')
def get_most_commented_posts(count=3):
    comments_posts = Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return {'comments_posts':comments_posts}
