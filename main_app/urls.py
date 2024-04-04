from django.urls import path
from .views import Home, ChairList, ChairDetail, SightingsListCreate, SightingsDetail, DupeListCreate, DupeDetail, AddDupeToChair, RemoveDupeFromChair

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('chairs/', ChairList.as_view(), name='chair-list'),
  path('chairs/<int:id>/', ChairDetail.as_view(), name='chair-detail'),
  path('chairs/<int:chair_id>/sightings/', SightingsListCreate.as_view(), name='sightings-list-create'),
  path('chairs/<int:chair_id>/sightings/<int:id>/', SightingsDetail.as_view(), name='sightings-detail'),
  path('chairs/<int:chair_id>/dupe/', DupeListCreate.as_view(), name='dupe-list-create'),
  path('chairs/<int:chair_id>/dupe/<int:id>/', DupeDetail.as_view(), name='dupe-detail'),
  path('chairs/<int:chair_id>/add_dupe/<int:dupe_id>/', AddDupeToChair.as_view(), name='add-dupe-to-chair'),
  path('chairs/<int:chair_id>/remove_dupe/<int:dupe_id>/', RemoveDupeFromChair.as_view(), name='remove-dupe-from-chair'),



]



