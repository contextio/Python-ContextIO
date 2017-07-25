FROM python:3.6.2-alpine3.6

COPY . /opt/app
WORKDIR /opt/app

RUN pip install -r requirements.txt -r dev-requirements.txt

CMD ["nosetests", "-s"]
