from django.urls import path
from . import views


urlpatterns = [
    path('', views.chain_view, name='chain_view'),
]


