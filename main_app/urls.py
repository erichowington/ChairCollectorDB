from django.urls import path
from .views import Home, ChairList, ChairDetail, SightingsListCreate, SightingsDetail, DupeListCreate, DupeDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('chairs/', ChairList.as_view(), name='chair-list'),
  path('chairs/<int:id>/', ChairDetail.as_view(), name='chair-detail'),
  path('chairs/<int:chair_id>/sightings/', SightingsListCreate.as_view(), name='sightings-list-create'),
  path('chairs/<int:chair_id>/sightings/<int:id>/', SightingsDetail.as_view(), name='sightings-detail'),
  path('chairs/<int:chair_id>/dupe/', DupeListCreate.as_view(), name='dupe-list-create'),
  path('chairs/<int:chair_id>/dupe/<int:id>/', DupeDetail.as_view(), name='dupe-detail'),

]



