FROM opensvc/python-connexion:latest

LABEL maintainer="support@opensvc.com"

WORKDIR /usr/src/app

COPY src /usr/src/app/

ENTRYPOINT ["python", "app.py"]
