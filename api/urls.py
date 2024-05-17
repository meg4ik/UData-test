from django.urls import path
from .views import AllProducts, ProductDetails, ProductDetail

urlpatterns = [
    path('all_products/', AllProducts.as_view(), name='all_products'),
    path('products/<str:product_uuid>/', ProductDetails.as_view(), name='product_details'),
    path('products/<str:product_uuid>/<str:product_field>/', ProductDetail.as_view(), name='product_field_detail'),
]