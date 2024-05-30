FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt-get update && apt-get install -y iputils-ping

COPY ./app /code/app
EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]