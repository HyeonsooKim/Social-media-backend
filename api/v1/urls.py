# api.v1.urls.py
# Django
from django.urls import path, include

urlpatterns = [
    path('user/', include('api.v1.user.urls')),
]