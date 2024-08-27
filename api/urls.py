from django.urls import path
from .views import Resultados

urlpatterns = [
  path('resultado/', Resultados.as_view(), name='resultado')
]