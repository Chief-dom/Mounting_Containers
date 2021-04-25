# Dockerfile, Image, Container
FROM ubuntu:20.04

RUN apt update && apt -y upgrade
RUN apt install -y python3-pip
# RUN apt install build-essential libssl-dev libffi-dev python3-dev
# RUN apt install -y python3-venv
# RUN python3 -m venv my_env
# RUN source my_env/bin/activate



WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt
EXPOSE 8501

# ENTRYPOINT ["streamlit", "run"]
# CMD ["dashboard.py"]