from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, CustomerBehaviorViewSet, PurchaseRecordViewSet,
    RecentActivityViewSet, CustomerInsightViewSet, CustomerKPIViewSet
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'behavior', CustomerBehaviorViewSet, basename='customer-behavior')
router.register(r'purchases', PurchaseRecordViewSet, basename='purchase-record')
router.register(r'activities', RecentActivityViewSet, basename='recent-activity')
router.register(r'insights', CustomerInsightViewSet, basename='customer-insight')
router.register(r'kpis', CustomerKPIViewSet, basename='customer-kpi')

urlpatterns = [
    path('', include(router.urls)),
]
