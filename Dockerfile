FROM python:3.9-alpine3.13
LABEL maintainer="ashishkarhale"

ENV PYTHONUNBUFFERED 1

RUN apk add --upgrade --no-cache postgresql-client && \
    apk add --upgrade --no-cache --virtual .temp-build-dir \
        build-base postgresql-dev musl-dev 

COPY ./requirements.txt ./tmp/requirements.txt
COPY ./requirements.dev.txt ./tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000
ARG DEV=false
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN if [ $DEV=true ];\
        then pip install -r /tmp/requirements.dev.txt; \
    fi 
RUN rm -rf /tmp 
RUN apk del .temp-build-dir
    
RUN adduser \
        --disabled-password\
        --no-create-home\
        django-user

USER django-user
