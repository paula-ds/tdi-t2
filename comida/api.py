from comida.models import Hamburguesa, Ingrediente
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import HamburguesaSerializer, IngredienteSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from datetime import datetime

#No olvidar poner / al final de las rutas


class HamburguesaViewSet(viewsets.ViewSet):
    def list(self, request): #obtener todas las hambuguesas
        queryset = Hamburguesa.objects.all()
        serializer = HamburguesaSerializer(queryset, many = True)
        ingredients = serializer.data

        path=request.build_absolute_uri()
        h=[i for i, x in enumerate(path) if x == "/"]
        correcto=path[:h[2]+1]
        n=-1
        for hamburger in queryset:
            ingredientes = []
            n+=1
            for ing in hamburger.ingredientes.all():
                ingredientes.append({'path':u'{0}ingrediente/{1}'.format(correcto, ing.id)})
            ingredients[n]["ingredientes"]=ingredientes

        response = Response(ingredients, status=200)
        response.reason_phrase= "resultados obtenidos"
        return response

    def create(self, request): #POST
        #campos vacíos
        for i in request.data.values():
            if not i:
                response = Response(status=400)
                response.reason_phrase= "input invalido"
                return response

        #para que no cree hamburguesa si hay atributos demás
        one=request.data.keys()
        two= all(elem in ["descripcion","nombre","precio","imagen"] for elem in one)
        if not two or len(one)!=4:
            response = Response(status=400)
            response.reason_phrase= "input invalido"
            return response

        #se crea
        serializer = HamburguesaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data,status=201)
            response.reason_phrase= "hamburguesa creada"
            return response

        response = Response(status=400)
        response.reason_phrase= "input invalido"
        return response
    
    def retrieve(self, request, pk=None): #GET
        if not pk.isnumeric():
            response = Response(status=400)
            response.reason_phrase= "id invalido"
            return response
        try:
            hamburger = Hamburguesa.objects.get(pk=pk)
        except Hamburguesa.DoesNotExist:
            response = Response(status=404)
            response.reason_phrase= "hamburguesa inexistente"
            return response
        serializer = HamburguesaSerializer(hamburger)
        #####mostrando bonito
        ingredients = serializer.data
        ingredientes = []
        path=request.build_absolute_uri()
        h=[i for i, x in enumerate(path) if x == "/"]
        correcto=path[:h[2]+1]

        for ing in hamburger.ingredientes.all():
            ingredientes.append({'path':u'{0}ingrediente/{1}'.format(correcto, ing.id)})
        ingredients["ingredientes"]=ingredientes

        response = Response(ingredients,status=200)
        response.reason_phrase= "operacion exitosa"
        return response
  
    def partial_update(self, request, pk=None):  #PATCH
        #campos vacíos
        for i in request.data.values():
            if not i:
                response = Response(status=400)
                response.reason_phrase= "Parámetros inválidos"
                return response

        #veo si corresponden parámetros
        one=request.data.keys() 
        two=  all(elem in ["descripcion","nombre","precio","imagen"] for elem in one)
        if not two:
            response = Response(status=400)
            response.reason_phrase= "Parámetros inválidos"
            return response
        try:
            hamburguer = Hamburguesa.objects.get(pk=pk)
        except Hamburguesa.DoesNotExist:
            response = Response(status=404)
            response.reason_phrase= "Hamburguesa inexistente"
            return response

        serializer = HamburguesaSerializer(hamburguer, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            #####mostrando bonito
            ingredients = serializer.data
            ingredientes = []
            path=request.build_absolute_uri()
            h=[i for i, x in enumerate(path) if x == "/"]
            correcto=path[:h[2]+1]

            for ing in hamburguer.ingredientes.all():
                ingredientes.append({'path':u'{0}ingrediente/{1}'.format(correcto, ing.id)})
            ingredients["ingredientes"]=ingredientes

            response = Response(ingredients, status=200)
            response.reason_phrase= "operacion exitosa"
            return response

        response = Response(status=400)
        response.reason_phrase= "Parámetros inválidos"
        return response
    
    def delete(self, request, pk=None):  #DELETE
        try:
            existe_ham = Hamburguesa.objects.get(id=pk)   
        except Hamburguesa.DoesNotExist: 
            response = Response(status=404)
            response.reason_phrase= "hamburguesa inexistente"
            return response
        #eliminar
        existe_ham.delete()
        response = Response(status=200)
        response.reason_phrase= "hamburguesa eliminada"
        return response

    #hamburguesa/id/ingrediente/id, #oid= id ingrediente
    @action(methods=['delete', 'put'], detail=True, url_path='ingrediente/(?P<oid>\d+)', url_name='busqueda')
    def hola(self,request,pk=None, oid=None):
        a = ''
        if request.method == 'DELETE':
            a = 'DELETE'
            if not pk.isnumeric():
                response = Response(status=400)
                response.reason_phrase= "Id de hamburguesa inválido"
                return response
            try:
                existe_ham = Hamburguesa.objects.get(id=pk)   #hamburguesa
                existe_ing=Hamburguesa.objects.filter(ingredientes__pk=oid)  #toda hamburguesa que tenga el ingrediente
            except Hamburguesa.DoesNotExist: 
                response = Response(status=404)
                response.reason_phrase= "Hamburguesa inexistente"  #en el foro se señala que el 404 es para errores de id != int()
                return response
            
            if existe_ham in existe_ing:  #si la hamburguesa tiene el ingrediente
                ingredient = Ingrediente.objects.get(id=oid)
                existe_ham.ingredientes.remove(ingredient)
                response = Response(status=200)
                response.reason_phrase= "ingrediente retirado"
                return response
            response = Response(status=404)
            response.reason_phrase= "Ingrediente inexistente en la hamburguesa"
            return response

        else:
            a = 'PUT' 
            if not pk.isnumeric():
                response = Response(status=400)
                response.reason_phrase= "Id de hamburguesa inválido"
                return response            
            try:
                existe_ham = Hamburguesa.objects.get(id=pk)
                existe_ing = Ingrediente.objects.get(id=oid)
            except Ingrediente.DoesNotExist:
                response = Response(status=404)
                response.reason_phrase= "Ingrediente inexistente"
                return response          	

            except Hamburguesa.DoesNotExist:
                #en el foro se señala que el 404 es para errores de id != int()
                response = Response(status=404)
                response.reason_phrase= "Hamburguesa inexistente"
                return response    

            existe_ham.ingredientes.add(existe_ing)
            response = Response(status=201)
            response.reason_phrase= "Ingrediente agregado"  
            return response
       

class IngredienteViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Ingrediente.objects.all()
        serializer = IngredienteSerializer(queryset, many = True)
        response = Response(serializer.data, status=200)
        response.reason_phrase= "resultados obtenidos"
        return response
    
    def create(self, request):
        #campos vacíos
        for i in request.data.values():
            if not i:
                response = Response(status=400)
                response.reason_phrase= "Input invalido"
                return response

        # no crear ingrediente si hay atributos demás
        one=request.data.keys() 
        two= all(elem in ["descripcion","nombre"] for elem in one)
        if not two or len(one)!=2 :  #ifnottwo= sitengodesobra 
            response = Response(status=400)
            response.reason_phrase= "Input invalido"
            return response

        #esto es para que no tengan el mismo nombre, en la realidad no pasa
        #try:
        #    esta_ya = Ingrediente.objects.get(nombre=request.data["nombre"])
        #    return Response({200:"Ingrediente con nombre repetido, crea otro"})  #no es necesario, sacar
        #except Ingrediente.DoesNotExist:
        #    esta_ya= "no"
        #if esta_ya=="no":
        serializer = IngredienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=201)
            response.reason_phrase= "Ingrediente creado"
            return response

        response = Response(status=400)
        response.reason_phrase= "Input invalido"
        return response
    
    def retrieve(self, request, pk=None):  #GET
        if not pk.isnumeric():
            response = Response(status=400)
            response.reason_phrase= "id invalido"
            return response
        try:
            ingredient = Ingrediente.objects.get(pk=pk)
        except Ingrediente.DoesNotExist:
            response = Response(status=404)
            response.reason_phrase= "ingrediente inexistente"
            return response   
        serializer = IngredienteSerializer(ingredient)
        response = Response(serializer.data, status=200)
        response.reason_phrase= "operacion exitosa"
        return response

    def delete(self, request, pk=None): #eliminar solo si no está en ninguna hamburguesa
        if not pk.isnumeric():
            response = Response(status=400)
            response.reason_phrase= "id invalido"
            return response
        try:
            ingredient = Ingrediente.objects.get(pk=pk)
        except Ingrediente.DoesNotExist:
            response = Response(status=404)
            response.reason_phrase= "ingrediente inexistente"
            return response
        hamburguesas = Hamburguesa.objects.filter(ingredientes__pk=pk)
        if hamburguesas:
            response = Response(status=409)
            response.reason_phrase= "Ingrediente no se puede borrar, se encuentra presente en una hamburguesa"
            return response
        ingredient.delete()
        response = Response(status=200)
        response.reason_phrase= "ingrediente eliminado"
        return response
