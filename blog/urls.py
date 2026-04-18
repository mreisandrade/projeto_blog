from django.urls import path

# from blog.views import index, post, page, created_by, category, tag, search
from blog.views import (
    PostListView, PostDetailView, PageDetailView, 
    CreatedByListView, CategoryListView, TagListView, 
    SearchListView,
) 
    

# Namespace
app_name = 'blog'


urlpatterns = [
    # Functions Based Views
    # path('', index, name='index'),
    # Usando o slug para acessar o post
    # path('post/<slug:slug>/', post, name='post'),
    # path('page/<slug:slug>/', page, name='page'),
    # path('created_by/<int:author_pk>/', created_by, name='created_by'),
    # path('category/<slug:slug>/', category, name='category'),
    # path('tag/<slug:slug>/', tag, name='tag'),
    # path('search/', search, name='search'),

    # Classes Based Views
    # É necessário chamar o método as_view() pois o path espera
    # receber um callable
    path('', PostListView.as_view(), name='index'),
    path(
        'post/<slug:slug>/', 
        PostDetailView.as_view(), 
        name='post'
    ),
    path(
        'page/<slug:slug>/', 
        PageDetailView.as_view(), 
        name='page',
    ),
    path(
        'created_by/<int:author_pk>/', 
        CreatedByListView.as_view(), 
        name='created_by',
    ),
    path(
        'category/<slug:slug>/', 
        CategoryListView.as_view(), 
        name='category',
    ),
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag'),
    path('search/', SearchListView.as_view(), name='search'),
]
