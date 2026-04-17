from django.core.paginator import Paginator
from django.shortcuts import render
# Usado para condicionais com OU no Django
from django.db.models import Q

from blog.models import Post


PER_PAGE = 9


def index(request):
    # Posts
    # Os parênteses são usados apenas para quebrar a linha
    # posts = (
    #     Post
    #     .objects
    #     .filter(is_published=True)
    #     .order_by('-pk')
    # )
    posts = Post.objects.get_published() # type: ignore

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def created_by(request, author_pk):
    # Posts
    # Os parênteses são usados apenas para quebrar a linha
    posts = (
        Post
        .objects
        .get_published() # type: ignore
        # Os __ significa que está pegando o campo pk do created_by
        # (foreign key), neste caso
        .filter(created_by__pk=author_pk)
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def category(request, slug):
    # Posts
    # Os parênteses são usados apenas para quebrar a linha
    # Os __ significa que está pegando o campo slug da category
    # (foreign key), neste caso
    posts = (
        Post
        .objects
        .get_published() # type: ignore
        .filter(category__slug=slug)
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def tag(request, slug):
    # Posts
    # Os parênteses são usados apenas para quebrar a linha
    # Os __ significa que está pegando o campo slug da tag
    # (foreign key), neste caso
    posts = (
        Post
        .objects
        .get_published() # type: ignore
        .filter(tags__slug=slug)
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def search(request):
    search_value = request.GET.get('search', '').strip()

    # Posts
    # Os parênteses são usados apenas para quebrar a linha
    # Os __ significa que está pegando o campo slug da tag
    # (foreign key), neste caso
    posts = (
        Post
        .objects
        .get_published() # type: ignore
        .filter(
            # Dessa forma, seria o AND
            # title__icontains=search_value
            # Título contém search_value OU
            # O Q possibilita condicionais com o OU (|)
            Q(title__icontains=search_value) |
            # Excerto contém search_value OU
            Q(excerpt__icontains=search_value) |
            # Conteúdo contém search_value
            Q(content__icontains=search_value)
        )[0:PER_PAGE] # Pega apenas 9 valores
    )

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
        }
    )


def page(request, slug):
    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )


def post(request, slug):
    # Pegando o post
    post = Post.objects.get_published().filter(slug=slug).first() # type: ignore

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )
