FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

RUN python /code/manage.py migrate
RUN python /code/manage.py test

CMD python /code/manage.py runserver 0.0.0.0:8000