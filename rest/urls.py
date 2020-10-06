"""petfinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('advertisement',AnimalAdvertisementView,basename='advertisement')

urlpatterns=[
    path('news/',AnimalNewsView.as_view(),name='news'),
    path('advertisement/type/',AnimalAdvertisementTypeView.as_view(),name='advertisement_type'),
    path('advertisement/color/',AnimalAdvertisementColorView.as_view(),name='advertisement_color'),
    path('favorit/',FavoritAnimal.as_view(),name='advertisement_favorit'),
    path('comment/<pk>',CommentAnimal.as_view()),]+router.urls
