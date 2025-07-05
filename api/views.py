# from django.http import JsonResponse
from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.models import Product, Order
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser
)
from rest_framework.views import APIView
from api.filters import ProductFilter, InStockFilterBackend
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    # queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer
    filterset_class = ProductFilter 
    #alternative way to order and search
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend,
        ]
    search_fields = ['=name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.page_query_param = 'page_number'
    pagination_class.page_size_query_param = 'size'
    pagination_class.max_page_size = 4

    def create(self, request, *args, **kwargs):
        # print(request.data)
        return super().create(request, *args, **kwargs)
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE' ]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

class ProductInfoAPIView(APIView):
    def get(self, request):
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

# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializers({
#         'products' : products,
#         'count' : len(products),
#         'max_price' : products.aggregate(max_price=Max('price'))['max_price']
#     })
#     return Response(serializer.data)