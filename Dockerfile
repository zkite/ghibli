FROM python:3.7.7-alpine3.12
ADD . /ghibli
WORKDIR /ghibli
RUN apk update && apk add build-base
RUN pip install -r requirements.txt
CMD python manage.py runserver -h 0.0.0.0 -p 8000
EXPOSE 8000