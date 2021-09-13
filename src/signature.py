import hmac
import logging
import os
import connexion

secret = os.environ.get('SECRET')


def verify(func):
    def wrapper(*argv, **kwargs):
        if secret is None:
            logging.info("signature verify skipped (undefined SECRET env var)")
            return func(*argv, **kwargs)
        data = connexion.request.data
        _, request_digest = connexion.request.headers['X-Hub-Signature'].split('=')
        digest = hmac.new(secret.encode(), msg=data, digestmod='sha1').hexdigest()
        if request_digest != digest:
            return {"message": "Invalid X-Hub-Signature"}, 403
        return func(*argv, **kwargs)

    return wrapper
