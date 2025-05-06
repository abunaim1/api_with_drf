# from django.http import JsonResponse
from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.models import Product, Order, OrderItem
from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductInfoSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics


class ProductListAPIView(generics.ListAPIView):
    # queryset = Product.objects.all()
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer
    
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializers({
        'products' : products,
        'count' : len(products),
        'max_price' : products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)



# Function Based Views.

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serialzer = ProductSerializer(products, many=True)
#     return Response(serialzer.data)


# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serialzer = ProductSerializer(product)
#     return Response(serialzer.data)

# @api_view(['GET'])
# def order_list(request):
#     # orders = Order.objects.prefetch_related(
#     #     'items', 'items__product',
#     # ).all()
#     orders = Order.objects.prefetch_related('items__product') # Both are same. This is perfect. 

#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


# def product_list(request):
#     products = Product.objects.all()
#     serialzer = ProductSerializer(products, many=True)
#     return JsonResponse(
#         {
#             'data' : serialzer.data
#         }
#     )

