# Dockerfile, Image, Container
FROM ubuntu:20.04

RUN apt update && apt -y upgrade
RUN apt install -y python3-pip

WORKDIR /opt
COPY requirements.txt .
COPY .streamlit .

RUN pip3 install -r requirements.txt
EXPOSE 8501
