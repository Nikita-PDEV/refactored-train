from django.shortcuts import render, get_object_or_404  
from .models import Post  

def news_list(request):  
    news = Post.objects.filter(post_type=Post.NEWS).order_by('-created_at')  
    return render(request, 'news/news_list.html', {'news': news})  

def news_detail(request, id):  
    post = get_object_or_404(Post, id=id)  
    return render(request, 'news/news_detail.html', {'post': post})  