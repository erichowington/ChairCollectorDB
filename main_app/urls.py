from django.urls import path
from .views import Home, ChairList, ChairDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('chairs/', ChairList.as_view(), name='chair-list'),
  path('chairs/<int:id>/', ChairDetail.as_view(), name='chair-detail'),

]



