# Generated by Django 5.0.3 on 2024-03-12 11:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя категории')),
                ('slug', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['name'], name='shop_catego_name_289c7e_idx')],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя')),
                ('slug', models.SlugField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='products/%Y/%m/%d', verbose_name='Фото')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость')),
                ('availabe', models.BooleanField(default=True, verbose_name='В наличии')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['id', 'slug'], name='shop_produc_id_f21274_idx'), models.Index(fields=['name'], name='shop_produc_name_a2070e_idx'), models.Index(fields=['-created'], name='shop_produc_created_ef211c_idx')],
            },
        ),
    ]
