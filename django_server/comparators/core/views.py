from rest_framework import viewsets
from .models import Product, Store, RelStorePrice, Capacity, UnitOfMeasure, TaxeRate
from .serializers import (
    ProductSerializer, StoreSerializer, RelStorePriceSerializer,
    CapacitySerializer, UnitOfMeasureSerializer, TaxeRateSerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category', 'state', 'capacity', 'unit_of_measure')
    serializer_class = ProductSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class RelStorePriceViewSet(viewsets.ModelViewSet):
    queryset = RelStorePrice.objects.select_related('product', 'store', 'taxe_rate')
    serializer_class = RelStorePriceSerializer

class CapacityViewSet(viewsets.ModelViewSet):
    queryset = Capacity.objects.all()
    serializer_class = CapacitySerializer

class UnitOfMeasureViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer

class TaxeRateViewSet(viewsets.ModelViewSet):
    queryset = TaxeRate.objects.all()
    serializer_class = TaxeRateSerializer