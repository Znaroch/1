from django_filters import FilterSet, DateFilter
from .models import Post

from django import forms


class PostFilter(FilterSet):
    date = DateFilter(
        widget=forms.DateInput(format='%d %m %Y', attrs={'type': 'date'}),
        field_name='date',
        lookup_expr='date__gte',
        label='Позже этой даты:',
    )
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author__user': ['exact'],
        }
