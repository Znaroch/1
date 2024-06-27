from django.urls import path
from allauth.account.views import LogoutView
from .views import PostList, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostSearch, IndexView, \
    upgrade_me, CategoryListView, subscribe

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='news_detail'),
    path('create/', PostCreateView.as_view(), name='news_add'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='news_edit'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='news_delete'),
    path('search/', PostSearch.as_view(), name='search'),
    path('home/', PostList.as_view(), name='home'),
    path('profile/', IndexView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),

]
