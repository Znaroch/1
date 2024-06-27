from .models import Post, Category
from modeltranslation.translator import register, TranslationOptions

@register(Post)#Регистрирую модель для перевода
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text') #указываю поля для перевода

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)