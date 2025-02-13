from rest_framework import serializers
from .models import Product, Store, RelStorePrice, Capacity, UnitOfMeasure, TaxeRate

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class RelStorePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelStorePrice
        fields = '__all__'

class CapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Capacity
        fields = '__all__'

class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = '__all__'

class TaxeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxeRate
        fields = '__all__'