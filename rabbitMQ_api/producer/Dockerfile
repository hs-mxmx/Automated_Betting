
FROM python:3.7-alpine

LABEL MAINTAINER "d.perezmoreno"

ARG BASE_DIR="/app"

ENV MY_MODULE="producer"

# RUN apt-get update -y && \
#     apt-get install -y python-pip python-dev

RUN apk add --no-cache --update \
    python3 python3-dev gcc g++ libc-dev 

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt ${BASE_DIR}/requirements.txt 

ADD . ${BASE_DIR}/${MY_MODULE}

ENV PYTHONPATH=$PYTHONPATH:${BASE_DIR}
ENV PYTHONPATH=${PYTHONPATH}:${MY_MODULE}
ENV AMQP_URL='amqp://xxalaqou:dQFGDDlp-pfhSolv57XHhVWeqmzcmD6l@crow.rmq.cloudamqp.com/xxalaqou'

WORKDIR ${BASE_DIR}

RUN pip3 install --upgrade pip setuptools wheel && \
    pip install -r ${BASE_DIR}/requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "/app/producer/src/producer.py" ]
