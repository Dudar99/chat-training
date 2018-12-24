FROM python:3.6.1
COPY requirements.txt /app/requirements.txt
WORKDIR /app/
RUN  apt-get install redis-server
RUN pip install -r requirements.txt
RUN pip install redis