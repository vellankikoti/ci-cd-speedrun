FROM python:3.9-slim
WORKDIR /app
RUN pip install flask redis sqlalchemy pymysql psutil requests cryptography
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]
