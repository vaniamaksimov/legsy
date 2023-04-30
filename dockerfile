FROM python:3.11

RUN mkdir alembic

COPY alembic/. alembic/.
COPY alembic.ini .
COPY .env .

RUN mkdir legsy

COPY legsy/requirements.txt legsy/

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r legsy/requirements.txt --no-cache-dir

COPY legsy/. legsy/
