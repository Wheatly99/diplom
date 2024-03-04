FROM python:3.10
EXPOSE 8501
WORKDIR /app
COPY . .
RUN chmod u+r+x pipeline.sh
ENTRYPOINT ["./pipeline.sh"]
