FROM python:3.9

ENV PYTHONUNBUFFERED=1

ARG BACKEND_URL 

ENV VARIABLE=$BACKEND_URL

WORKDIR /code

COPY requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

COPY . $BACKEND_URL

EXPOSE $BACKEND_URL

CMD ["sh", "-c","python manage.py runserver 0.0.0.0:${VARIABLE}"]
