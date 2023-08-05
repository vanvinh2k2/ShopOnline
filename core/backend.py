from taggit.models import Tag
from django.db.models import Avg, Count
from django.contrib import messages
from .models import Product, Category, \
Vendor, CartOrder, CartOrderItems, ProductImage, \
ProductReview, Wishlish, Address;
from userauths.models import Profile
from .forms import ProductReviewForm
import calendar
from django.db.models.functions import ExtractMonth

from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm

from rest_framework import status, permissions, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view

class CategoryAPI(generics.RetrieveAPIView, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialize
    lookup_field = 'cid'

    def get(self, request, *args, **kwargs):
        cid = kwargs.get('cid')
        if cid is not None:
            instance = self.get_object()
            serializer = CategorySerialize(instance, context={'request': request})
            return Response({
                    'success' : True,
                    'message' : 'Get Category success.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
        else: 
            instance = self.get_queryset()
            serializer = self.serializer_class(instance, many=True, context={'request':request})
            return Response({
                    'success' : True,
                    'message' : 'Get list Category success.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

class VendorAPI(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerialize
    lookup_field = 'vid'

    def get(self, request, *args, **kwargs):
        vid = kwargs.get('vid')
        if vid is not None:
            instance = self.get_object()
            serializer = VendorSerialize(instance, context={'request':request})
            return Response({
                    'success' : True,
                    'message' : 'Get Vendor success.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
        else:
            instance = self.get_queryset()
            serializer = self.serializer_class(instance, many=True, context={'request':request})
            return Response({
                    'success' : True,
                    'message' : 'Get list Vendor success.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
    
class ProductAPI(generics.RetrieveAPIView, generics.ListAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerialize
    lookup_field = 'pid'

    def get(self, request, *args, **kwargs):
        pid = kwargs.get('pid')
        if pid is not None:
            instance = self.get_object()
            serializer = ProductSerialize(instance, context={'request':request})
            return Response({
                    'success' : True,
                    'message' : 'Get Vendor success.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
        else:
            instance = self.get_queryset()
            serializer = self.serializer_class(instance, many=True, context={'request':request})
            return Response({
                        'success' : True,
                        'message' : 'Get list Vendor success.',
                        'data': serializer.data
                    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_product_review(request, *args, **kwargs):
    pid = kwargs.get('pid')
    product = Product.objects.get(pid=pid)
    productreview = ProductReview.objects.filter(product=product)
    serializer = ProductReviewSerialize(productreview, many=True)
    return Response({
                        'success' : True,
                        'message' : 'Get list review success.',
                        'data': serializer.data
                    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_product_review(request, *args, **kwargs):
    pid = kwargs.get('pid')
    id = kwargs.get('id')
    review = request.data.get('review')
    rating = request.data.get('rating')
    user = User.objects.get(pk=id)
    product = Product.objects.get(pid=pid)
    productreview = ProductReview.objects.get(user=user, product=product)
    if productreview is None:
        productreview = ProductReview.objects\
            .create(user=user, 
                    product=product, 
                    review=review, 
                    rating=rating)
        serializer = ProductReviewSerialize(productreview)
        return Response({
                            'success' : True,
                            'message' : 'Add review success.',
                            'data': serializer.data
                        }, status=status.HTTP_200_OK)
    serializer = ProductReviewSerialize(productreview)
    return Response({
                        'success' : False,
                        'message' : 'You have already rated this product.',
                        'data': serializer.data
                    }, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def search(request, *args, **kwargs):
    q = request.data.get('q')
    if q is not None:
        product = Product.objects.filter(title__icontains=q)
    else: product = Product.objects.all()
    serialize = ProductSerialize(product, context={'request' : request}, many=True)
    return Response({
        'success' : True,
        'message' : 'Search success.',
        'data' : serialize.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def filter_category(request, *args, **kwargs):
    cid = kwargs.get('cid')
    category = Category.objects.get(cid=cid)
    product = Product.objects.filter(category=category)
    serialize = ProductSerialize(product, context={'request' : request}, many=True)
    return Response({
        'success' : True,
        'message' : 'Filter success.',
        'data' : serialize.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def cart(request, *args, **kwargs):
    uid = kwargs.get('id')
    user = User.objects.get(pk=uid)
    cartorder = CartOrder.objects.filter(user=user)
    if cartorder is None:
        return Response({
            'success' : False,
            'message' : 'Cart is nothing!'
        }, status=status.HTTP_200_OK)
    else:
        serialize = CartOrderSerialize(cartorder, context={'request': request}, many=True)
        return Response({
            'success' : True,
            'message' : 'Filter success.',
            'data' : serialize.data
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
def cart_detail(request, *args, **kwargs):
    oid = kwargs.get('oid')
    cartorder = CartOrder.objects.get(oid=oid)
    cartorderdetail = CartOrderItems.objects.filter(order=cartorder)
    serialize = CartOrderItemsSerialize(cartorderdetail, context={'request': request}, many=True)
    return Response({
        'success' : True,
        'message' : 'Filter success.',
        'data' : serialize.data
    }, status=status.HTTP_200_OK)