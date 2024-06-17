from datetime import date

from django import forms
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'type' , 'category']

    #def clean(self):
     #   cleaned_data = super().clean()
      #  author = cleaned_data.get("author")
       # today = date.today()
        #post_limit = Post.objects.filter(author=author, time_in__date=today).count()
        #if post_limit >= 3:
         #   raise ValidationError("Нельзя публиковать больше трех постов в сутки!")
        #return cleaned_data




class MyCustomSignupForm(SignupForm):

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        return user
        common = Group.objects.get(name='common')
        common.user_set.add(user)