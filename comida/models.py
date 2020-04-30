from django.db import models

# Create your models here.

class Ingrediente(models.Model):
    nombre= models.CharField(max_length=100)
    descripcion=models.CharField(max_length=500)  

class Hamburguesa(models.Model):
    nombre= models.CharField(max_length=100)
    precio=models.IntegerField()
    descripcion=models.CharField(max_length=500)
    imagen=models.URLField(max_length=200)
    ingredientes = models.ManyToManyField(Ingrediente, blank=True)

    