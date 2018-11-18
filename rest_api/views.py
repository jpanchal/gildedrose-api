from rest_framework import generics, permissions
from .permissions import IsOwner
from .serializers import ItemlistSerializer, UserSerializer, CartSerializer
from .models import Itemlist, Cart
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import status


class CreateView(generics.ListCreateAPIView):
    """This class handles the GET and POSt requests of our rest api."""
    queryset = Itemlist.objects.all()
    serializer_class = ItemlistSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwner)

    def perform_create(self, serializer):
        """Save the post data when creating a new itemlist."""
        serializer.save(owner=self.request.user)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles GET, PUT, PATCH and DELETE requests."""

    queryset = Itemlist.objects.all()
    serializer_class = ItemlistSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)


class CartCreateView(generics.ListCreateAPIView):
    """This class handles the GET and POSt requests of our rest api."""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)

    def perform_create(self, serializer):
        """Save the post data when creating a new itemlist."""
        serializer.save(owner=self.request.user)


class CartDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles GET, PUT, PATCH and DELETE requests."""

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)


class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
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