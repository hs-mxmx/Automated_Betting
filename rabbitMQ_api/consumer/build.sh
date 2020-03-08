#!/bin/bash
app="consumer"
docker build -t ${app}:latest .
docker run -d \
    -p 7000:7000 \
    ${app} 
