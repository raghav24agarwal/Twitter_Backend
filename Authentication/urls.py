from django.urls import include, path
from Authentication import views

from django.urls import path


urlpatterns = [
    path('', views.home , name ='home'),
    path('signup/', views.signup , name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin/', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
]