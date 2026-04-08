from site_setup.models import SiteSetup

# Context Processors
# Injeta variáveis nos templates (ex.: request.user)
# Função que recebe uma request e devolve um dicionário
# É configurado dentro do settings.py
def site_setup(request):
    # Dados coletados do model SiteSetup
    setup = SiteSetup.objects.order_by('-id').first()

    # Variáveis que podem ser usadas dentro dos templates
    return {
        'site_setup': setup,
    }
