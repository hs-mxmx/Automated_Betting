#!/bin/bash
app="task_api"
docker build -t ${app}:latest .
docker run -d \
    -p 8080:8080 \
    ${app} 
