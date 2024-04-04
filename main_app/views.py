from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .models import Chair, Sightings, Dupe
from .serializers import UserSerializer, ChairSerializer, SightingsSerializer, DupeSerializer

class Home(APIView):
  def get(self, request):
    content = {'message': 'This is the Chair-Collecter API Root'}
    return Response(content)
  
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })
    
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
  
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })
  
class ChairList(generics.ListCreateAPIView):
  serializer_class = ChairSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
      # This ensures we only return cats belonging to the logged-in user
      user = self.request.user
      return Chair.objects.filter(user=user)

  def perform_create(self, serializer):
      # This associates the newly created cat with the logged-in user
      serializer.save(user=self.request.user)
      
      
class ChairDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ChairSerializer
  lookup_field = 'id'

  def get_queryset(self):
    user = self.request.user
    return Chair.objects.filter(user=user)

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    dupes_not_associated = Dupe.objects.exclude(id__in=instance.dupes.all())
    dupes_serializer = DupeSerializer(dupes_not_associated, many=True)

    return Response({
        'chair': serializer.data,
        'dupes_not_associated': dupes_serializer.data
    })

  def perform_update(self, serializer):
    chair = self.get_object()
    if chair.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to edit this chair."})
    serializer.save()

  def perform_destroy(self, instance):
    if instance.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to delete this chair."})
    instance.delete()
    
    

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
  
class DupeList(generics.ListCreateAPIView):
  queryset = Dupe.objects.all()
  serializer_class = DupeSerializer
  
  
class DupeDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Dupe.objects.all()
  serializer_class = DupeSerializer
  lookup_field = 'id'

  
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


