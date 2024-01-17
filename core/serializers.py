from djoser.serializers import UserSerializer  as BaseUserSerialized, UserCreateSerializer as BaseUserCreate
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreate):
    class Meta(BaseUserCreate.Meta):
        fields = ['id','username','password','email','first_name','last_name']

class UserSerializer(BaseUserSerialized):
    class Meta(BaseUserSerialized.Meta):
        fields = ['id','username','email','first_name', 'last_name']