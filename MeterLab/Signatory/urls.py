from django.urls import path, include


from . import views
from .views import *

urlpatterns = [
    # path('', Signs.as_view(), name='signatory'),
    path('', views.Signatories, name='signatory'),
]
