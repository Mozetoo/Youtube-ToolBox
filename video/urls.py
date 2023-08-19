from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('download/', views.download, name='download'),
    path('search/<str:video_id>/', views.download_v, name='video'),

]
