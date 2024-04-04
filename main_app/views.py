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
  
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    
    dupes_not_associated = Dupe.objects.exclude(id__in=instance.dupes.all())
    dupes_serializer = DupeSerializer(dupes_not_associated, many=True)

    return Response({
        'chair': serializer.data,
        'dupes_not_associated': dupes_serializer.data
    })

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
  
class AddDupeToChair(APIView):
  def post(self, request, chair_id, dupe_id):
    chair = Chair.objects.get(id=chair_id)
    dupe = Dupe.objects.get(id=dupe_id)
    chair.dupe.add(dupe)
    return Response({'message': f' Dupe has been logged for {chair.model}'})
  
class RemoveDupeFromChair(APIView):
  def post(self, request, chair_id, dupe_id):
    chair = Chair.objects.get(id=chair_id)
    dupe = Dupe.objects.get(id=dupe_id)
    chair.dupe.remove(dupe)
    return Response({'message': f'Dupe has been removed from {chair.model}'})


