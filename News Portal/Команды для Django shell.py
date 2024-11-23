python manage.py shell  
Затем выполните следующие команды:

python
from django.contrib.auth.models import User  
from your_app_name.models import Author, Category, Post, Comment  

#1 Создаем двух пользователей  
user1 = User.objects.create_user('user1', password='password123')  
user2 = User.objects.create_user('user2', password='password123')  

#2 Создаем два объекта модели Author, связанные с пользователями  
author1 = Author.objects.create(user=user1)  
author2 = Author.objects.create(user=user2)  

#3 Добавляем 4 категории в модель Category  
category1 = Category.objects.create(name='Спорт')  
category2 = Category.objects.create(name='Политика')  
category3 = Category.objects.create(name='Образование')  
category4 = Category.objects.create(name='Технологии')  

#4 Добавляем 2 статьи и 1 новость  
post1 = Post.objects.create(author=author1, title='Спортивные достижения', content='Текст статьи о спорте', post_type=Post.ARTICLE)  
post2 = Post.objects.create(author=author1, title='Новые технологии', content='Текст статьи о технологиях', post_type=Post.ARTICLE)  
post3 = Post.objects.create(author=author2, title='Политическая ситуация', content='Текст новости о политике', post_type=Post.NEWS)  

#5 Присваиваем категории (в одной должно быть не меньше 2 категорий)  
post1.categories.add(category1, category4)  # Статья с 2 категориями  
post2.categories.add(category4)  # Статья с 1 категорией  
post3.categories.add(category2)  # Новость с 1 категорией  

#6 Создаем как минимум 4 комментария к разным объектам модели Post  
comment1 = Comment.objects.create(post=post1, user=user1, text='Комментарий к статье 1')  
comment2 = Comment.objects.create(post=post1, user=user2, text='Еще один комментарий к статье 1')  
comment3 = Comment.objects.create(post=post2, user=user1, text='Комментарий к новости 1')  
comment4 = Comment.objects.create(post=post3, user=user2, text='Комментарий к статье 2')  

#7. Применяем функции like() и dislike() к статьям и комментариям  
post1.like()  # Увеличиваем рейтинг  
comment1.like()  

post2.dislike()  # Уменьшаем рейтинг  
comment3.dislike()  

#8. Обновляем рейтинги пользователей  
author1.update_rating()  
author2.update_rating()  

#9. Вывести username и рейтинг лучшего пользователя  
best_author = Author.objects.order_by('-rating').first()  
print(best_author.user.username, best_author.rating)  

#10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи  
best_post = Post.objects.order_by('-rating').first()  
print(best_post.created_at, best_post.author.user.username, best_post.rating, best_post.title, best_post.preview())  

#11. Выводим все комментарии к этой статье  
comments = Comment.objects.filter(post=best_post)  
for comment in comments:  
    print(comment.created_at, comment.user.username, comment.rating, comment.text)  