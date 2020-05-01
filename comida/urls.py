from comida import api
from rest_framework.routers import DefaultRouter
from django.urls import path, include

#Crear router y registrar las vistas
router = DefaultRouter(trailing_slash=False)
router.register(r'hamburguesa', api.HamburguesaViewSet, 'comida')
router.register(r'ingrediente', api.IngredienteViewSet, 'ingrediente')

urlpatterns = router.urls
