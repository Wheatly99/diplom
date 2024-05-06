FROM python:3.10
EXPOSE 8501
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y docker.io
CMD ["python3", "main.py"]
