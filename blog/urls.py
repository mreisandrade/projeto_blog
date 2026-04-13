from django.urls import path

from blog.views import index, post, page


# Namespace
app_name = 'blog'


urlpatterns = [
    path('', index, name='index'),
    # Usando o slug para acessar o post
    path('post/<slug:slug>/', post, name='post'),
    path('page/', page, name='page'),
]
