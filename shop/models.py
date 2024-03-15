from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя категории')
    slug = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name='Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE,
                                 verbose_name='Категория')
    '''взаимосвязь один-ко-многим. товар принадлежит одной категории, а категория содержит к несколько товарам'''
    name = models.CharField(max_length=200, verbose_name='Имя')
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Фото')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Стоимость')
    availabe = models.BooleanField(default=True, verbose_name='В наличии')#наличие или отсутствие
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    updated = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.pk, self.slug])