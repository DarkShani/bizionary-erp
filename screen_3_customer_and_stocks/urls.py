from django.urls import path, include

urlpatterns = [
    path('customer-analytics/', include('screen_3_customer_and_stocks.customer_analytics.urls')),
]
