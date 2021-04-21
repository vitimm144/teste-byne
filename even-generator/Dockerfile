FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /app_even

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 80
EXPOSE 5000

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app_even/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /app_even

ENTRYPOINT [ "python", "app.py" ]