FROM python:3.8.3-alpine
# set work directory
WORKDIR app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
# copy project

#COPY ./entrypoint.sh .
# copy project
COPY .. .
# run entrypoint.sh
#ENTRYPOINT ["./entrypoint.sh"]