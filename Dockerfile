FROM python:3.9-alpine3.13
LABEL maintainer="ashishkarhale"

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt ./tmp/requirements.txt
COPY ./requirements.dev.txt ./tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000
ARG DEV=false

RUN apk add --upgrade --no-cache postgresql-client && \
    apk add --upgrade --no-cache --virtual .temp-build-deps \
        build-base postgresql-dev musl-dev 

RUN pip install -r /tmp/requirements.txt

RUN if [ $DEV=true ];\
        then pip install -r /tmp/requirements.dev.txt; \
    fi 
RUN rm -rf /tmp && \
    apk del .temp-build-deps
    
RUN adduser \
        --disabled-password\
        --no-create-home\
        django-user

USER django-user
