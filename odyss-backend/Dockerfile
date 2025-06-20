FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements/base.txt

ENV FLASK_APP=run.py

CMD ["flask", "run", "--host=0.0.0.0"]
