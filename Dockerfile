FROM python:3.12-slim

RUN apt update -y && apt install awscli -y
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN pip install --upgrade accelerate

ENV PORT=8080
EXPOSE 8080

CMD ["python3", "app.py"]