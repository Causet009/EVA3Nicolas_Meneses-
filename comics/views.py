from django.shortcuts import render

from .models import Comic


def catalogo(request):
    comics = Comic.objects.filter(disponible=True)

    return render(
        request,
        'comics/catalogo.html',
        {
            'comics': comics
        }
    )