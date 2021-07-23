# syntax=docker/dockerfile:1

FROM python:3

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

RUN chmod -R 755 /code/static/
RUN chown -R "$USER":www-data /code/

EXPOSE 8000
