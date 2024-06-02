FROM python:3.11

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --upgrade --no-cache-dir
RUN apt-get update && apt-get install -y cron

COPY . .

ENV TZ=Asia/Taipei
RUN python3 setup_cron.py
CMD [ "gunicorn", "--bind", "0.0.0.0:5000","app:app"]
