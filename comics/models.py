from django.db import models


class Editorial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Comic(models.Model):
    editorial = models.ForeignKey(
        Editorial,
        on_delete=models.CASCADE,
        related_name='comics'
    )

    titulo = models.CharField(max_length=150)
    numero_tomo = models.PositiveIntegerField()
    precio = models.PositiveIntegerField()
    tapa_dura = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True)
    portada = models.ImageField(
        upload_to='portadas/',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return f"{self.titulo} - Tomo {self.numero_tomo}"