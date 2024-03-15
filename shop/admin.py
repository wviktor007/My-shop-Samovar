from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategotyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}#Автоматически создавать "slug" по имени



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'availabe', 'created', 'updated']
    list_filter = ['availabe', 'created', 'updated']
    list_editable = ['price', 'availabe']#возможность редактировать в админке
    prepopulated_fields = {'slug': ('name',)}#Автоматически создавать "slug" по имени