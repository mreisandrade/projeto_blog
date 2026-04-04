from django.urls import path

from blog.views import index


# Namespace
app_name = 'blog'


urlpatterns = [
    path('', index, name='index'),
]
