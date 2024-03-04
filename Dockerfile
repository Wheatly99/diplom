FROM python:3.10
EXPOSE 8501
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]
