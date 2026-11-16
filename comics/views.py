import uuid

from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReservaForm
from .models import Comic, Editorial


def catalogo(request):
    comics = Comic.objects.filter(disponible=True)

    busqueda = request.GET.get('q', '')
    editorial_id = request.GET.get('editorial', '')

    if busqueda:
        comics = comics.filter(titulo__icontains=busqueda)

    if editorial_id:
        comics = comics.filter(editorial_id=editorial_id)

    editoriales = Editorial.objects.all()

    return render(
        request,
        'comics/catalogo.html',
        {
            'comics': comics,
            'editoriales': editoriales,
            'busqueda': busqueda,
            'editorial_seleccionada': editorial_id,
        }
    )


def detalle_comic(request, comic_id):
    comic = get_object_or_404(
        Comic,
        id=comic_id,
        disponible=True
    )

    if request.method == 'POST':
        formulario = ReservaForm(request.POST)

        if formulario.is_valid():
            reserva = formulario.save(commit=False)
            reserva.comic = comic
            reserva.codigo = uuid.uuid4().hex[:10].upper()
            reserva.save()

            return redirect(
                'detalle_comic',
                comic_id=comic.id
            )

    else:
        formulario = ReservaForm()

    return render(
        request,
        'comics/detalle.html',
        {
            'comic': comic,
            'formulario': formulario,
        }
    )