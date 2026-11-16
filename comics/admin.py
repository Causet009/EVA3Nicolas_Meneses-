from django.contrib import admin

from .models import Comic, Editorial


@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'editorial',
        'numero_tomo',
        'stock',
        'precio_clp',
        'tapa_dura',
        'disponible',
    )

    list_filter = (
        'editorial',
        'tapa_dura',
        'disponible',
    )

    search_fields = (
        'titulo',
    )

    @admin.display(description='Precio')
    def precio_clp(self, obj):
        return f"${obj.precio:,.0f}".replace(',', '.')