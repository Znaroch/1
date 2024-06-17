from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post, Category

from django.views.decorators.cache import cache_page

import logging.getLogger(__name__)


def index(request):
    logger.info('INFO')
    news_portal = news_portal.objects.all()
    return render(request, 'index.html', context={'news_portal': news_portal})

logger = logging
@cache_page (60 * 15)


class NewsList(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = '-time_in'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

class NewsCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    context_object_name = 'posts'
    permission_required = ('news_portal.add_post')


    def form_valid(self, form):
        post = form.save(commit=False)
        today = date.today()
        post_limit = Post.objects.filter(author=post.author, time_in__date=today).count()
        if post_limit >= 3:
            return render(self.request, 'post_limit.html', {'author': post.author})
        post.save()
        return super().form_valid()

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    context_object_name = 'posts'
    permission_required = ('news_portal.change_post')

    def get_queryset(self):
        posts = Post.objects.filter(type='NW').order_by('-time_in')
        return posts

class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'posts'
    succes_url = reverse_lazy('post_list')


class ArticleCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'
    context_object_name = 'posts'
    permission_required = ('news_portal.change_post')

class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'article_edit.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(type='AR').order_by('-time_in')
        return posts

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'arcticle_delete.html'
    context_object_name = 'posts'
    succes_url = reverse_lazy('post_list')

def author_now(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        user.groups.add(author_group)
    return redirect('post_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'news_portal/subscribe.html', {'category': category, 'message': message})