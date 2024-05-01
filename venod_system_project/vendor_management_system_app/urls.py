
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vendors/post/', create_vendor, name='create_vendor'),
    path('api/vendors/list_vendors/', list_vendors, name='list_vendors'),
    path('api/vendors/get_vendor/', get_vendor, name='get_vendors'),
    path('api/vendors/update_vendor/<int:vendor_id>/', update_vendor, name='update_vendor'),
    path('api/vendors/delete_vendor/<int:vendor_id>/', delete_vendor, name='delete_vendor'),
    path('api/purchase_orders/ create_purchase_order/', create_purchase_order, name='create_purchase_order'),
    path('api/purchase_orders/list_purchase_orders/', list_purchase_orders, name='list_purchase_orders'),
    path('api/purchase_orders/get_purchase_order/<int:po_id>/', get_purchase_order, name='retrieve_purchase_order'),
    path('api/purchase_orders/update_purchase_order/<int:po_id>/', update_purchase_order, name='update_purchase_order'),
    path('api/purchase_orders/delete_purchase_order/<int:po_id>/', delete_purchase_order, name='delete_purchase_order'),
    path('api/vendors/get_historical_performance/<int:vendor_id>/', get_historical_performance, name='get_historical_performance'),
    path('api/historical_performance/create_historical_performanc/', create_historical_performance, name='create_historical_performance'),
    path('api/historical_performance/ update_historical_performance/<int:hp_id>/', update_historical_performance, name='update_historical_performance'),
    path('api/historical_performance/delete_historical_performance/<int:hp_id>/', delete_historical_performance, name='delete_historical_performance'),

]
