from rest_framework import serializers
from .models import Chair, Sightings, Dupe

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
        
class SightingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sightings
        fields = '__all__'
        read_only_fields = ('chair',)
        
