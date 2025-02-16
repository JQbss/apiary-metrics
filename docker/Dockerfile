FROM python:3.12.6-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY /requirements/base.txt .
RUN pip install --no-cache-dir -r base.txt

COPY .. .
