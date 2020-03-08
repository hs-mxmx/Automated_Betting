
FROM python:3.7-alpine

LABEL MAINTAINER "d.perezmoreno"

ARG BASE_DIR="/app"

ENV MY_MODULE="consumer"

# RUN apt-get update -y && \
#     apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt ${BASE_DIR}/requirements.txt 

ADD ${MY_MODULE} ${BASE_DIR}/${MY_MODULE}

ENV PYTHONPATH=$PYTHONPATH:${BASE_DIR}
ENV PYTHONPATH=${PYTHONPATH}:${MY_MODULE}

WORKDIR ${BASE_DIR}

RUN pip install -r ${BASE_DIR}/requirements.txt && \
    pwd && \
    ls  

ENTRYPOINT [ "python" ]

CMD [ "/app/consumer/src/consumer.py" ]
