import uuid

from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReservaForm
from .models import Comic, Editorial, Reserva


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
            cantidad = formulario.cleaned_data['cantidad']

            if comic.stock == 0:
                formulario.add_error(
                    'cantidad',
                    'Este cómic está agotado.'
                )

            elif cantidad > comic.stock:
                formulario.add_error(
                    'cantidad',
                    f'Solo hay {comic.stock} unidades disponibles.'
                )

            else:
                reserva = formulario.save(commit=False)
                reserva.comic = comic
                reserva.codigo = uuid.uuid4().hex[:10].upper()
                reserva.save()

                comic.stock -= cantidad
                comic.save()

                return redirect(
                    'comprobante',
                    codigo=reserva.codigo
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


def comprobante(request, codigo):
    reserva = get_object_or_404(
        Reserva,
        codigo=codigo
    )

    total = reserva.comic.precio * reserva.cantidad

    return render(
        request,
        'comics/comprobante.html',
        {
            'reserva': reserva,
            'total': total,
        }
    )