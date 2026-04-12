from django.contrib import admin

from blog.models import Tag, Category, Page


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
class PageyAdmin(admin.ModelAdmin):
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
