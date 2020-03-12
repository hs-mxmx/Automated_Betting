
FROM python:3.7-alpine

LABEL MAINTAINER "d.perezmoreno"

ARG BASE_DIR="/app"

ENV MY_MODULE="task_api"

# RUN apt-get update -y && \
#     apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt ${BASE_DIR}/requirements.txt 

ADD ${MY_MODULE} ${BASE_DIR}/${MY_MODULE}

ENV PYTHONPATH=$PYTHONPATH:${BASE_DIR}
ENV PYTHONPATH=${PYTHONPATH}:${MY_MODULE}

WORKDIR ${BASE_DIR}/${MY_MODULE}

RUN pip install -r ${BASE_DIR}/requirements.txt && \
    cd ${BASE_DIR}/${MY_MODULE}

ENTRYPOINT [ "python" ]

CMD [ "/app/task_api/src/main.py" ]
