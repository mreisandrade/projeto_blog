from typing import Any

from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import render
# Usado para condicionais com OU no Django
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
# Para usar Classes Based Views no Django
from django.views.generic import ListView

from blog.models import Post, Page


PER_PAGE = 9

'''
Funtion Based Views -> São funções
    - Mais usadas em aplicações simples
Class Based Views -> São classes (POO)
    - Para lógicas mais complicadas
    - Deixa o código mais limpo, simples e fácil de testar
    - Permite reutilizar código

Obs.: As classes based views do Django JÁ TEM PAGINAÇÃO, ou 
não é necessário implementar isso, como foi feito anteriormente.

Link para classes base do Django:
https://docs.djangoproject.com/pt-br/4.2/ref/class-based-views/
    - DetailView: 1 valor
    - ListView: lista de valores
'''


# def index(request):
#     # Posts
#     # Os parênteses são usados apenas para quebrar a linha
#     # posts = (
#     #     Post
#     #     .objects
#     #     .filter(is_published=True)
#     #     .order_by('-pk')
#     # )
#     posts = Post.objects.get_published() # type: ignore

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': 'Home - ',
#         },
#     )

# Class Based View equivalente a função "index"
class PostListView(ListView):
    # É necessário informar o model que está sendo usado
    model = Post
    # Por padrão, o Django tenta carregar um template padrão
    # Por tanto, é necessário alterar o template
    # Dica: Use seus próprios nomes, não os padrões do Django,
    # neste caso
    template_name = 'blog/pages/index.html'
    # Definindo o nome do contexto enviado para o template
    # Variável dentro do context
    context_object_name = 'posts'
    # Configurando a ordenação
    ordering = '-pk',
    # A paginação já está pronta no Class Based View
    # É necessário apenas informar quanto elementos por página
    paginate_by = PER_PAGE
    # Definindo a QuerySet filtrar apenas os posts que estão 
    # publicados. Outra forma é sobreescrever o método
    # get_queryset(), como mostrado abaixo
    queryset = Post.objects.get_published() # type: ignore


    # Sobrescrevendo o método que opera o contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # print()
        # print(context)
        # print()

        # Atualizando o contexto com o título da página
        context.update(
            {
                'page_title': 'Home - ',
            }
        )

        return context
    

    # Sobrescrevendo o método que opera a QuerySet
    # Para filtrar apenas os posts que estão publicados
    # def get_queryset(self):
    #     queryset =  super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset
    

def created_by(request, author_pk):
    # Buscando o usuário no model User
    user = User.objects.filter(pk=author_pk).first()
    
    if user is None:
        raise Http404()
    
    user_full_name = user.username
    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'

    page_title = f'Posts de {user_full_name} - '

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
            'page_title': page_title,
        },
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

    if len(page_obj) == 0:
        raise Http404()

    page_title = f'{page_obj[0].category.name} - Categoria - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        },
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

    if len(page_obj) == 0:
        raise Http404()

    page_title = f'{page_obj[0].tags.first().name} - Tag - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
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

    # Pega, no máximo, 30 caracteres
    page_title = f'{search_value[:30]} - Search - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
        },
    )


def page(request, slug):
    # Pegando o post
    page_object = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first() 
    ) # type: ignore

    if page_object is None:
        raise Http404()

    page_title = f'{page_object.title} - Página - '

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_object,
            'page_title': page_title,
        },
    )


def post(request, slug):
    # Pegando o post
    post_object = Post.objects.get_published().filter(slug=slug).first() # type: ignore

    if post_object is None:
        raise Http404()

    page_title = f'{post_object.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_object,
            'page_title': page_title,
        },
    )
