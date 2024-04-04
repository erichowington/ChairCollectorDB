from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Chair, Sightings, Dupe
from .serializers import ChairSerializer, SightingsSerializer, DupeSerializer

class Home(APIView):
  def get(self, request):
    content = {'message': 'This is the Chair-Collecter API Root'}
    return Response(content)
  
class ChairList(generics.ListCreateAPIView):
  queryset = Chair.objects.all()
  serializer_class = ChairSerializer

class ChairDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Chair.objects.all()
  serializer_class = ChairSerializer
  lookup_field = 'id'

class SightingsListCreate(generics.ListCreateAPIView):
  serializer_class = SightingsSerializer

  def get_queryset(self):
    chair_id = self.kwargs['chair_id']
    return Sightings.objects.filter(chair_id=chair_id)

  def perform_create(self, serializer):
    chair_id = self.kwargs['chair_id']
    chair = Chair.objects.get(id=chair_id)
    serializer.save(chair=chair)
    
class SightingsDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = SightingsSerializer
  lookup_field = 'id'

  def get_queryset(self):
    chair_id = self.kwargs['chair_id']
    return Sightings.objects.filter(chair_id=chair_id)
  
class DupeListCreate(generics.ListCreateAPIView):
  serializer_class = DupeSerializer

  def get_queryset(self):
    chair_id = self.kwargs['chair_id']
    return Dupe.objects.filter(chair_id=chair_id)

  def perform_create(self, serializer):
    chair_id = self.kwargs['chair_id']
    chair = Chair.objects.get(id=chair_id)
    serializer.save(chair=chair)
    
class DupeDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = DupeSerializer
  lookup_field = 'id'

  def get_queryset(self):
    chair_id = self.kwargs['chair_id']
    return Dupe.objects.filter(chair_id=chair_id)

