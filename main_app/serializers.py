from rest_framework import serializers
from .models import Chair

class ChairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chair
        fields = '__all__'
        