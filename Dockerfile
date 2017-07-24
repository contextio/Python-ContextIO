FROM python:3.6.2-alpine3.6

COPY ./requirements.txt /tmp
COPY ./dev-requirements.txt /tmp

RUN pip install -r /tmp/dev-requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /opt/app
WORKDIR /opt/app

CMD ["nosetests", "-s"]