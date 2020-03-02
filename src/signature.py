import hmac
import os
import connexion

secret = os.environ.get('SECRET', 'This is not a secret')


def verify(func):
    def wrapper(*argv, **kwargs):
        data = connexion.request.data
        _, request_digest = connexion.request.headers['X-Hub-Signature'].split('=')
        digest = hmac.new(secret.encode(), msg=data, digestmod='sha1').hexdigest()
        if request_digest != digest:
            return {"message": "Invalid X-Hub-Signature"}, 403
        return func(*argv, **kwargs)

    return wrapper
