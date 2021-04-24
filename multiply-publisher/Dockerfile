FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /app_multiply

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 80


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app_multiply/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /app_multiply

ENTRYPOINT [ "python", "app.py" ]