from rest_framework import serializers
from .models import Itemlist, Cart
from django.contrib.auth.models import User


class ItemlistSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Itemlist
        fields = ('id', 'name', 'description', 'quantity', 'price', 'owner')
        # read_only_fields = ('date_created', 'date_modified')

class CartSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Cart
        fields = ('id', 'item', 'quantity', 'owner')

class UserSerializer(serializers.ModelSerializer):
    """A user serializer to aid in authentication and authorization."""

    itemlists = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Itemlist.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'itemlists')
