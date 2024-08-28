FROM python:3.6.4-alpine3.7
RUN apk update
RUN apk add --no-cache --virtual .build-deps
RUN apk add --no-cache --virtual libc-dev
RUN apk add --no-cache --virtual python3-dev
RUN apk add --no-cache --virtual gcc
RUN apk add --no-cache --virtual musl-dev
RUN apk add --no-cache --virtual postgresql-dev
ADD . /telle-ai-daemon
WORKDIR /telle-ai-daemon
RUN pip install -r requirements.txt --no-cache-dir
RUN apk del --no-cache .build-deps
ENTRYPOINT ["python"]
CMD ["-u", "app.py"]