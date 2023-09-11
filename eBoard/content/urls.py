from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from . import views
from accounts.views import SignUp

urlpatterns = [
	path('', AnnounceList.as_view(), name='announce_list'),
	path('my_announces/', MyAnnounces.as_view(), name='my_announces'),
	path('reacts_to_my_announces', ReactionList.as_view(), name='reacts_to_announces'),
	path('<int:pk>/', AnnounceDetail.as_view(), name='announce_detail'),
	path('reacts/<int:pk>/', ReactDetail.as_view(), name='react_detail'),
	path('create/', AnnounceCreate.as_view(), name='announce_create'),
	path('<int:pk>/leave_react/', ReactionCreate.as_view(), name='reaction_create'),
	path('<int:announce_id>/<int:react_id>/', views.react_accept, name='react-accept'),
	path('login/', auth_views.LoginView.as_view(), name='accounts/login'),
	path('logout/', auth_views.LogoutView.as_view(next_page='/enter'), name='logout'),
	path('registration', SignUp.as_view(), name='signing_up'),

]
