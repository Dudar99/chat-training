FROM python:3.6.1
COPY requirements.txt /app/requirements.txt
WORKDIR /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install psycopg2
RUN pip install redis
