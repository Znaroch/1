from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, Author

import pytz


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context



class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'all_news.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    current_time = timezone.now()
    timezones = pytz.common_timezones  # добавляем в контекст все доступные часовые пояса


    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs



@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    #что бы стать автором нужно не только добавить его в группу, но и создать модель автора
    #Создаю модель на основе этого пользователя, которого получаю через request
    Author.objects.create(user=user)
    return redirect('profile')

#Дженерик вывода 1 новости
class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    queryset = Post.objects.all()

#Дженерик создания новости
class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news_p.add_post',)
    template_name = 'news_add.html'
    form_class = PostForm

#дженерик изменения новости
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_p.change_post',)
    template_name = 'news_add.html'
    form_class = PostForm

    #метод get_object используется вместо queryset, что бы получить информацию об объекте
    #который буду редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


#Дженерик удаления объекта
class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


#Дженерик для поиска
class PostSearch(ListView):
    model = Post
    ordering = '-date'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET,  queryset)
        if self.request.GET:
            return self.filterset.qs
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context



class CategoryListView(PostList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date')
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
    return render(request, 'subscribe.html', {'category': category, 'message': message})

