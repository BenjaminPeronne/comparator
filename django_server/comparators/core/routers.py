from rest_framework.routers import DefaultRouter
from .views import CapacityViewSet, UnitOfMeasureViewSet, TaxeRateViewSet

router = DefaultRouter()
router.register(r'capacities', CapacityViewSet, basename='capacity')
router.register(r'units-of-measure', UnitOfMeasureViewSet, basename='unit_of_measure')
router.register(r'taxe-rates', TaxeRateViewSet, basename='taxe_rate')
