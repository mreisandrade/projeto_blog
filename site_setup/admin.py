from django.contrib import admin
from django.http import HttpRequest
from site_setup.models import MenuLink, SiteSetup


# Mostrar os elementos de MenuLink em SiteSetup
class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    # Quantidade de campos extras que aparece
    extra = 1


# Register your models here.
# @admin.register(MenuLink)
# class MenuLinkAdmin(admin.ModelAdmin):
#     list_display = 'id', 'text', 'url_or_path'
#     list_display_links = 'id', 'text', 'url_or_path'
#     search_fields = 'id', 'text', 'url_or_path'


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description'
    inlines = MenuLinkInline,

    # Esse método verifica se o usuário tem permissão para 
    # adicionar itens no model 
    def has_add_permission(self, request: HttpRequest) -> bool:
        # Tem que retornar True ou False
        # Verifica se há algum objeto no model
        return not SiteSetup.objects.exists()
