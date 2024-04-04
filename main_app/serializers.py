from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Chair, Sightings, Dupe

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )
      
      return user

class DupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dupe
        fields = '__all__'
        read_only_fields = ('chair',)

class ChairSerializer(serializers.ModelSerializer):
    dupes = DupeSerializer(many=True, read_only=True)
    class Meta:
        model = Chair
        fields = '__all__'
        user = serializers.PrimaryKeyRelatedField(read_only=True)
        
class SightingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sightings
        fields = '__all__'
        read_only_fields = ('chair',)
        
