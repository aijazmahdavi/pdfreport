from django.urls import path
from .views import *

urlpatterns = [
    path('', renderpdf, name='index'),
    path('generate-report/', generate_report, name='generate_report'),
]
