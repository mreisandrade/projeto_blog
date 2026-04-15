from django.contrib import admin
# Para Django Summernote
from django_summernote.admin import SummernoteModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

from blog.models import Tag, Category, Page, Post


# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # Campos mostrados
    list_display = 'id', 'name', 'slug'
    # Campos com link para abrir a edição dos dados
    list_display_links = 'name',
    # Campos usados nas pesqueisas
    search_fields = 'id', 'name', 'slug'
    # Quantidade de dados por páginas
    list_per_page = 10
    # Ordem apresentada (ordem decrescente por id)
    ordering = '-id',
    # Completa automaticamente o campo, neste caso, o slug
    # o nome da tag
    prepopulated_fields = {
        "slug": ('name',),
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Campos mostrados
    list_display = 'id', 'name', 'slug'
    # Campos com link para abrir a edição dos dados
    list_display_links = 'name',
    # Campos usados nas pesqueisas
    search_fields = 'id', 'name', 'slug'
    # Quantidade de dados por páginas
    list_per_page = 10
    # Ordem apresentada (ordem decrescente por id)
    ordering = '-id',
    # Completa automaticamente o campo, neste caso, o slug
    # o nome da tag
    prepopulated_fields = {
        "slug": ('name',),
    }


@admin.register(Page)
# class PageyAdmin(admin.ModelAdmin):
class PageyAdmin(SummernoteModelAdmin):
    # Campos mostrados
    list_display = 'id', 'title', 'slug'
    # Campos com link para abrir a edição dos dados
    list_display_links = 'title',
    # Campos usados nas pesqueisas
    search_fields = 'id', 'title', 'slug'
    # Quantidade de dados por páginas
    list_per_page = 10
    # Ordem apresentada (ordem decrescente por id)
    ordering = '-id',
    # Completa automaticamente o campo, neste caso, o slug
    # o nome da tag
    prepopulated_fields = {
        "slug": ('title',),
    }

    # Informando quais campos usam summernote
    summernote_fields = 'content',


@admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
class PostAdmin(SummernoteModelAdmin):
    # Campos mostrados
    list_display = 'id', 'title', 'is_published', 'created_by'
    # Campos com link para abrir a edição dos dados
    list_display_links = 'title',
    # Campos usados nas pesqueisas
    search_fields = 'id', 'title', 'slug', 'excerpt', 'content', 'created_by'
    # Quantidade de dados por páginas
    list_per_page = 50
    # Lista de filtros
    list_filter = 'category', 'is_published'
    # O que vai ser editável na tabela
    list_editable = 'is_published',
    # Ordem apresentada (ordem decrescente por id)
    ordering = '-id',
    # Campos somente para leitura
    readonly_fields = 'created_at', 'updated_at', 'updated_by', 'created_by', 'link'
    # Completa automaticamente o campo, neste caso, o slug
    # o nome da tag
    prepopulated_fields = {
        "slug": ('title',),
    }

    autocomplete_fields = 'tags', 'category'

    # Informando quais campos usam summernote
    summernote_fields = 'content',


    # Funciona como um atributo da classe post 
    # Apenas para a página do admin
    def link(self, obj):
        # Verifica se o objeto já foi criado (tem primary key)
        if not obj.pk:
            return '-'

        # Pega a url do post (serm definir get_absolute_url no model)
        # post_url = reverse('blog:post', args=(obj.slug,))
        # Pega a url do post, depois de definida get_absolute_url no model)
        post_url = obj.get_absolute_url()

        # Isso não é renderizado automaticamente por segurança
        # É necessário marcar a string como segura com o 
        # mark_safe
        safe_link = mark_safe(
            f'<a target="_blank" href="{post_url}">Ver post</a>'
        )
        
        return safe_link


    # Sobreescrevendo o método save_model para atribuir os 
    # campos updated_by e created_by
    # request: requisição que está sendo feito
    # obj: objeto que está sendo modificado
    # form: formulário utilizado
    # change: verdadeiro quando estiver alterando o objeto
    def save_model(self, request, obj, form, change):
        # Caso esteja apenas atualizando o post
        if change:
            obj.updated_by =  request.user
        else:
            obj.created_by =  request.user

        # Salva o objeto
        obj.save()
