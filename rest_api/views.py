from rest_framework import generics, permissions
from .permissions import IsOwner
from .serializers import ItemlistSerializer, UserSerializer, CartSerializer
from .models import Itemlist, Cart
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import status


class CreateView(generics.ListCreateAPIView):
    """
        GET itemlists/
        POST itemlists/
    """
    queryset = Itemlist.objects.all()
    serializer_class = ItemlistSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwner)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
       GET itemlists/:id/
       PUT itemlists/:id/
       DELETE itemlists/:id/
    """

    queryset = Itemlist.objects.all()
    serializer_class = ItemlistSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)


class CartCreateView(generics.ListCreateAPIView):
    """
        GET buyitem/
        POST buyitem/
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CartDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
       GET buyitem/:id/
       PUT buyitem/:id/
       DELETE buyitem/:id/
    """

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)


class UserView(generics.ListAPIView):
    """
       GET users/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
    """
       GET users/:id/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterUsers(generics.CreateAPIView):
    """
        POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        if not username and not password:
            return Response(
                data={
                    "message": "username and password is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )