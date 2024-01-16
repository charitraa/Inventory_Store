from djoser.serializers import UserCreateSerializer as BaseUserCreate
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreate):
    class Meta(BaseUserCreate.Meta):
        fields = ['id','username','password','email','first_name','last_name']
