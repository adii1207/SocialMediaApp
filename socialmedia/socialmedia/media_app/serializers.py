from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import FriendRequest

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)

        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class FriendRequestSerializer(serializers.ModelSerializer):
    from_username = serializers.SerializerMethodField()
    to_username = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = "__all__"
    
    def get_from_username(self, obj):
        return obj.from_user.username

    def get_to_username(self, obj):
        return obj.to_user.username
