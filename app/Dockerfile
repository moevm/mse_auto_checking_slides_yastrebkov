FROM python:3.6.8-alpine3.9

LABEL MAINTAINER="John Doe anton.yastrebkoff@gmail.com"

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

# Install Python dependencies
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip install --upgrade pip
RUN pip install -U setuptools
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers
RUN apk del build-deps
ADD ./requirements.txt /var/www/requirements.txt
RUN pip install -r requirements.txt
ADD . /var/www/
RUN pip install gunicorn
RUN pip install dataclasses


RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www

EXPOSE 5000

CMD gunicorn --chdir /var/www wsgi:app -w 1 -b 0.0.0.0:5000 --reload


