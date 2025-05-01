# from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer
from api.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serialzer = ProductSerializer(products, many=True)
    return Response(serialzer.data)

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serialzer = ProductSerializer(product)
    return Response(serialzer.data)


# Old
# def product_list(request):
#     products = Product.objects.all()
#     serialzer = ProductSerializer(products, many=True)
#     return JsonResponse(
#         {
#             'data' : serialzer.data
#         }
#     )