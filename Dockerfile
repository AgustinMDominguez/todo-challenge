FROM python:3.9.6-slim-buster

RUN pip install --upgrade pip

RUN mkdir /app

COPY . /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN ./manage.py migrate

EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]
