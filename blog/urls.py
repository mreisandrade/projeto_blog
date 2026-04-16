from django.urls import path

from blog.views import index, post, page, created_by, category


# Namespace
app_name = 'blog'


urlpatterns = [
    path('', index, name='index'),
    # Usando o slug para acessar o post
    path('post/<slug:slug>/', post, name='post'),
    path('page/<slug:slug>/', page, name='page'),
    path('created_by/<int:author_pk>/', created_by, name='created_by'),
    path('category/<slug:slug>/', category, name='category'),
]
