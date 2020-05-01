from rest_framework import serializers
from comida.models import Hamburguesa, Ingrediente


class IngredienteSerializer(serializers.ModelSerializer):
    #url=HyperlinkedIdentityField(view_name='ingrediente',lookup_filed)
    class Meta:
        model= Ingrediente
        fields = '__all__'

class HamburguesaSerializer(serializers.ModelSerializer):
    #ingredientes =  IngredienteSerializer(many=true, read_only=True)
    class Meta:
        model= Hamburguesa
        fields = '__all__'
