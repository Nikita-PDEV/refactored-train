from django.db import models  
from django.contrib.auth.models import User  
from django.db.models import Sum, F, Count  
from django.utils import timezone  

class Author(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    rating = models.IntegerField(default=0)  

    def update_rating(self):  
        # Сумма рейтингов всех статей автора (умноженная на 3)  
        post_ratings = Post.objects.filter(author=self).aggregate(total=Sum('rating'))['total'] or 0  
        # Сумма рейтингов всех комментариев автора  
        comment_ratings = Comment.objects.filter(user=self.user).aggregate(total=Sum('rating'))['total'] or 0  
        # Сумма рейтингов всех комментариев к статьям автора  
        post_comments_ratings = Comment.objects.filter(post__author=self).aggregate(total=Sum('rating'))['total'] or 0  
        
        self.rating = post_ratings * 3 + comment_ratings + post_comments_ratings  
        self.save()  

class Category(models.Model):  
    name = models.CharField(max_length=255, unique=True)  

class Post(models.Model):  
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  
    ARTICLE = 'AR'  
    NEWS = 'NW'  
    POST_TYPE_CHOICES = [  
        (ARTICLE, 'Article'),  
        (NEWS, 'News'),  
    ]  
    post_type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES)  
    created_at = models.DateTimeField(auto_now_add=True)  
    categories = models.ManyToManyField('Category', through='PostCategory')  
    title = models.CharField(max_length=255)  
    content = models.TextField()  
    rating = models.IntegerField(default=0)  

    def preview(self):  
        return self.content[:124] + '...' if len(self.content) > 124 else self.content  

    def like(self):  
        self.rating += 1  
        self.save()  

    def dislike(self):  
        self.rating -= 1  
        self.save()  

class PostCategory(models.Model):  
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  

class Comment(models.Model):  
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  
    rating = models.IntegerField(default=0)  

    def like(self):  
        self.rating += 1  
        self.save()  

    def dislike(self):  
        self.rating -= 1  
        self.save()  