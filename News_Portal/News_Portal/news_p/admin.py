from django.contrib import admin
from .models import Post, Category
from modeltranslation.admin import TranslationAdmin

'''
class PostAdmin(admin.ModelAdmin, TranslationAdmin):
    list_display = ('title', 'text', 'date', 'type', 'rating')
    list_filter = ('title', 'date', 'type', 'rating', )
    search_fields = ('title', 'category__name', 'author__user__username')#через поле автора обращаюсь к юзеру и уже к имени

class CategoryAdmin(admin.ModelAdmin, TranslationAdmin):
    list_display = ('name',)
    list_filter = ('subscribers',)
'''
class PostAdmin(TranslationAdmin):
    model = Post

class CategoryAdmin(TranslationAdmin):
    model = Category

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)