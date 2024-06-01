FROM python:3.11

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV TZ=Asia/Taipei

CMD [ "gunicorn", "--bind", "0.0.0.0:5000","app:app"]
