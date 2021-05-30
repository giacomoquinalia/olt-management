FROM python:3.8

# Do not generate .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Do not store log messages in buffers, messages are sent imidiatly
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN pip install -r requirements/requirements.txt
