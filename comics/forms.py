import re

from django import forms

from .models import Reserva


def validar_rut_chileno(rut):
    patron = r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$'

    if not re.match(patron, rut):
        raise forms.ValidationError(
            'Ingrese el RUT con formato 12.345.678-5.'
        )

    rut_limpio = rut.replace('.', '').replace('-', '')
    cuerpo = rut_limpio[:-1]
    dv_ingresado = rut_limpio[-1].upper()

    suma = 0
    multiplicador = 2

    for numero in reversed(cuerpo):
        suma += int(numero) * multiplicador
        multiplicador += 1

        if multiplicador > 7:
            multiplicador = 2

    resto = 11 - (suma % 11)

    if resto == 11:
        dv_correcto = '0'
    elif resto == 10:
        dv_correcto = 'K'
    else:
        dv_correcto = str(resto)

    if dv_ingresado != dv_correcto:
        raise forms.ValidationError(
            'El RUT ingresado no es válido.'
        )

    return rut


class ReservaForm(forms.ModelForm):
    cantidad = forms.IntegerField(
        min_value=1,
        max_value=3,
        label='Cantidad'
    )

    class Meta:
        model = Reserva
        fields = [
            'nombre',
            'email',
            'rut',
            'cantidad',
        ]

        labels = {
            'nombre': 'Nombre',
            'email': 'Correo electrónico',
            'rut': 'RUT',
        }

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre completo'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'correo@ejemplo.com'
                }
            ),
            'rut': forms.TextInput(
                attrs={
                    'placeholder': '12.345.678-5'
                }
            ),
        }

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        return validar_rut_chileno(rut)