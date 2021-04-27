FROM python:3.8.1

RUN apt-get update
RUN apt-get install build-essential
# set work directory
WORKDIR /multiply_api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 80
EXPOSE 8000
EXPOSE 8001
EXPOSE 8002

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /multiply_api/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /multiply_api

ENTRYPOINT [ "crossbar", "start" ]