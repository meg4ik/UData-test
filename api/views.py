import json
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .serializers import ProductSerializer

# Create your views here.
class AllProducts(APIView):
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'mcdonalds_menu.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            serializer = ProductSerializer(data, many=True)
            return Response(serializer.data)
        except FileNotFoundError:
            return Response({'detail': 'File not found'}, status=404)
        
        
class ProductDetails(APIView):
    def get(self, request, product_uuid):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'mcdonalds_menu.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            product = next((item for item in data if item['uuid'] == product_uuid), None)
            if product:
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Product not found'}, status=404)
        except FileNotFoundError:
            return Response({'detail': 'File not found'}, status=404)
        
    
class ProductDetail(APIView):
    def get(self, request, product_uuid, product_field):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'mcdonalds_menu.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            product = next((item for item in data if item['uuid'] == product_uuid), None)
            if product:
                if product_field in product:
                    return Response({product_field: product[product_field]})
                else:
                    return Response({'detail': 'Field not found in product'}, status=404)
            else:
                return Response({'detail': 'Product not found'}, status=404)
        except FileNotFoundError:
            return Response({'detail': 'File not found'}, status=404)