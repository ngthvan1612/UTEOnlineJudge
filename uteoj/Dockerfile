# syntax=docker/dockerfile:1

FROM python:3

RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y openjdk-11-jdk mono-mcs && \
    apt-get clean;

RUN adduser --disabled-password --gecos '' uteoj_compiler
RUN adduser --disabled-password --gecos '' uteoj_run

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONWARNINGS="ignore"

WORKDIR /code/
ENV MEDIA_ROOT=/code/judge_data/
ENV PRODUCT_UTE_ONLINE_JUDGE=1

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

RUN python /code/manage.py collectstatic --noinput --clear

RUN chmod -R 0755 /code/static/
RUN chown -R "$USER":www-data /code/
RUN chmod +x /code/libjudger/libjudger.so

EXPOSE 8000
