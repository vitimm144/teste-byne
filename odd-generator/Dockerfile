FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /app_odd

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 80
EXPOSE 5001

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app_odd/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /app_odd

ENTRYPOINT [ "python", "app.py" ]