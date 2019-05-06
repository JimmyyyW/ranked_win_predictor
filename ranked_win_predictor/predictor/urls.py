from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='predictor-home'),
    path('about/', views.about, name='predictor-about'),
    path('download/', views.download, name='predictor-download'),
]
