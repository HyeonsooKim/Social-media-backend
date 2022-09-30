# api.v1.user.tokens.py

# DRF
from rest_framework.exceptions import AuthenticationFailed
# Third Party
from decouple import config
import jwt
import datetime


def generate_token(payload, type):
    if type == "access":
        # 1시간
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    elif type == "refresh":
        # 1주
        exp = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    else:
        raise Exception("Invalid tokenType")
    
    payload['exp'] = exp
    payload['iat'] = datetime.datetime.utcnow()
    encoded = jwt.encode(payload, config("SECRET_KEY"), algorithm=config("ALGORITHM"))

    return encoded

def validate_token(access_token):
    if not access_token :
        raise AuthenticationFailed('UnAuthenticated!')

    try :
        payload = jwt.decode(access_token, config("SECRET_KEY"), algorithms=[config("ALGORITHM")])
        return payload

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('UnAuthenticated!')

