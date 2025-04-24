FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install nano

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED 1
ENV IS_DOCKER_USED 1

RUN echo "alias ll='ls -la'" >> /root/.bashrc

CMD bash -c "sleep 3 && \
             python manage.py makemigrations && \
             python manage.py migrate && \
             python manage.py runserver 0.0.0.0:8000"
