# api.v1.user.views.py
# DRF
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
# Third Party
import jwt
from decouple import config
# Internal
from apps.user.models import User
from .serializers import SignUpSerializer, SignInSerializers
from .tokens import generate_token, validate_token

class UserSignUpView(APIView):
    serializer_class = SignUpSerializer
    
    @action(methods=['POST'], detail=False)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            try:
                # payload에 넣을 값 커스텀 가능
                payload_value = user.id
                payload = {
                    "subject": payload_value,
                }

                access_token = generate_token(payload, "access")
                refresh_token = generate_token(payload, "refresh")

                res = Response(
                        {
                            "user": user.email,
                            "message": "register successs",
                            "token": {
                                "access": access_token,
                                "refresh": refresh_token,
                            },
                        },
                        status=status.HTTP_200_OK,
                    )

                #쿠키데이터 저장
                res.set_cookie("access", access_token, httponly=True)
                res.set_cookie("refresh", refresh_token, httponly=True)
                return res

            except User.DoesNotExist:

                data = {
                    "results": {
                        "msg": "유저 정보가 올바르지 않습니다.",
                        "code": "E4010"
                    }
                }

                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

            except Exception as e:
                print(e)
                data = {
                    "results": {
                        "msg": "정상적인 접근이 아닙니다.",
                        "code": "E5000"
                    }
                }

                return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSignInView(APIView):
    serializer_class = SignInSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.validated_data['user']
            access_token = serializer.validated_data['access']
            refresh_token = serializer.validated_data['refresh']

            res = Response(
                {
                    "user": user,
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            ) 

            #쿠키데이터 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView) :
    """
    유저 로그인여부 확인 뷰
    """
    def get(self,request):
        access_token = request.COOKIES.get('access')
        payload = validate_token(access_token)
        user = User.objects.filter(id=payload['subject']).first()
        serializer = SignInSerializers(user)
        return Response(serializer.data)


class UserSignoutView(APIView) :
    """
    로그아웃 뷰
    """
    def post(self,request):
        res = Response()
        res.delete_cookie('access')
        res.data = {
            "message" : 'Signout success'
        }

        return res