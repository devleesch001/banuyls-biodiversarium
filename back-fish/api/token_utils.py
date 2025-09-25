import datetime
import jwt

SECRET_KEY = "L\xed1y\xff5\xfb\xed\xa1\xd8&\xf9r\xc6c-[\xdfNJ\x17\x07''"

def encode_auth_token(user_id, grants=[]):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id,
            'scope':":".join(grants)
        }
        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
        return token
    except Exception as e:
        return e

def check_user_grants(token, g):
    return g in token["scope"].split(":")

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY 
            , algorithms='HS256')
        return payload
    except jwt.ExpiredSignatureError as e:
        print(e)
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError as e:
        print(e)
        return 'Invalid token. Please log in again.'

def check_token(request):
    # get the auth token
    auth_token = request.headers.get('Authorization')
    if auth_token:
        resp = decode_auth_token(auth_token)
        if not isinstance(resp, str):
            print(datetime.datetime.fromtimestamp(resp["exp"]), datetime.datetime.now())
            return datetime.datetime.fromtimestamp(resp["exp"]) > datetime.datetime.now()
    return False