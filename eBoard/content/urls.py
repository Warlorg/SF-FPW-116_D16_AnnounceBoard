from django.urls import path
from .views import *
from . import views


urlpatterns = [
	path('', AnnounceList.as_view(), name='announce_list'),
	path('<int:pk>/', AnnounceDetail.as_view(), name='announce_detail'),
	path('reacts/<int:pk>/', ReactDetail.as_view(), name='react_detail'),
	path('create/', AnnounceCreate.as_view(), name='announce_create'),
	path('<int:pk>/leave_react/', ReactionCreate.as_view(), name='reaction_create'),
	path('', views.react_accept, name='accept'),
]






