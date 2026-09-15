FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY sensor_generator.py .
RUN sleep 20
CMD ["python","sensor_generator.py"]
