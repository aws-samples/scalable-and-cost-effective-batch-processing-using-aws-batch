FROM python:3-slim

WORKDIR /var/app

COPY requirements.txt /var/app
RUN pip install -r requirements.txt

COPY . /var/app

ENTRYPOINT ["script/entrypoint"]