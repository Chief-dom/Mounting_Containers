# Dockerfile, Image, Container
FROM python:3.8

WORKDIR .

COPY requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["dashboard.py"]