from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from decimal import Decimal
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .models import Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    UserSerializer, ProductSerializer, CartSerializer, CartItemSerializer, 
    OrderItemSerializer, OrderSerializer, RegisterSerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST'])
    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity if not created else quantity
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'], url_path='remove')
    def remove_item(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            if cart_item.quantity > quantity:
                cart_item.quantity -= quantity
                cart_item.save()
                return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)
            else:
                cart_item.delete()
                return Response({'message': 'Cart item removed.'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['POST'], url_path='place')
    def place_order(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        total_price = Decimal('0.00')
        for item in cart.items.all():
            if item.quantity > item.product.stock:
                return Response(
                    {"error": f"Not enough stock for {item.product.name}."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            total_price += item.product.price * item.quantity

        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )

            item.product.stock -= item.quantity
            item.product.save()

        cart.items.all().delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]