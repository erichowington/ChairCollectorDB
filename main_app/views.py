from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Chair
from .serializers import ChairSerializer

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

