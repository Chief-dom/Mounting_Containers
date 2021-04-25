# Dockerfile, Image, Container
FROM ubuntu:20.04

RUN apt-get -y update
RUN apt-get install python3 -y

WORKDIR .

COPY requirements.txt ./
RUN pip3 install -r requirements.txt
EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["dashboard.py"]