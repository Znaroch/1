from django.contrib import admin
from django.urls import path, include
from .views import


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news_portal.urls')),
    path('accounts/', include('allauth.urls')),


    path('', .as_view()),
    path('<int:pk>/', cache_page(60*10)(View.as_view()), name='product_detail'),
    path('create/', View.as_view(), name='_create'),
    path('<int:pk>/update', View.as_view(), name='_update'),
    path('<int:pk>/delete', View.as_view(), name='_delete'),

]
