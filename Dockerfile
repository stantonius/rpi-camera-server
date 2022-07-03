FROM python:3.10-slim-bullseye
# FROM --platform=linux/amd64 python:3.9-slim-bullseye
LABEL maintainer="Craig Stanton"
WORKDIR /code
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/code"
EXPOSE 5454
COPY . /code/
RUN pip install --upgrade -r /code/requirements.txt
CMD uvicorn main:api --host 0.0.0.0 --port 5454 --reload