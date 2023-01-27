# Create your models here.

from django.contrib.auth import get_user_model
from django.db import models
from category.models import Category
from ckeditor.fields import RichTextField

User = get_user_model()


class Hotel(models.Model):
    STATUS_CHOISES=(
        ('in_stock', 'Есть свободные номера!'),
        ('out_of_stock', 'Свободных номеров нет!')
    )

    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='products')
    title = models.CharField(max_length=150)
    description = RichTextField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='images')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.CharField(choices=STATUS_CHOISES, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    average_rating = models.FloatField(verbose_name='Average_rating', default=0, )

    def __str__(self):
        return self.title


class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='comments',
                              on_delete=models.CASCADE)
    post = models.ForeignKey(Hotel, related_name='comments',
                             on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} -> {self.post} -> {self.created_at}'


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ['owner', 'post']


