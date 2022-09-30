# api.v1.user.urls.py

# Django
from django.urls import path, include
# DRF
from rest_framework.routers import DefaultRouter
# Internal
from .views import UserSignUpView, UserSignInView, UserView, UserSignoutView

router = DefaultRouter()

urlpatterns =[
    path('', include(router.urls)),
    # 회원가입/로그인
    path("sign-up/", UserSignUpView.as_view()),
    path("sign-in/", UserSignInView.as_view()),
    path("auth/", UserView.as_view()),
    path("sign-out/", UserSignoutView.as_view()),
]