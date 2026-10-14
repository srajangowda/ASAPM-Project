FROM python:3.12-slim

WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and artifacts
COPY . /app

ENV PORT=8080
EXPOSE 8080

CMD ["python3", "app.py"]