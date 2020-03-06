FROM python:2.7-alpine

LABEL MAINTAINER "d.perezmoreno"

ARG BASE_DIR="/app"

ENV PYTHONBUFFERED=1
ENV MY_MODULE="consumer"

COPY ../requirements.txt ${BASE_DIR}/${MY_MODULE}

ADD ${MY_MODULE} ${BASE_DIR}/${MY_MODULE}

ENV PYTHONPATH=$PYTHONPATH:${BASE_DIR}
ENV PYTHONPATH=${PYTHONPATH}:${MY_MODULE}

WORKDIR ${BASE_DIR}/${MY_MODULE}

RUN pip install -r ${BASE_DIR}/requirements.txt && \
    cd ${BASE_DIR}/${MY_MODULE}

ENTRYPOINT [ "python" ]

CMD [ "/app/consumer/src/consumer.py" ]
