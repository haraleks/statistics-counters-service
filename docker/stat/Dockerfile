ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}
ENV PYTHONUNBUFFERED 1
ARG PIP_EXTRA_INDEX_URL

RUN mkdir -p /code/
WORKDIR /code/

COPY sc_service/requirements.txt /code/

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

CMD gunicorn --reload --bind 0.0.0.0:8000 -w 1 -k uvicorn.workers.UvicornWorker sc_service.main:app
