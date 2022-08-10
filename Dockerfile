FROM python:3.8.3-slim
WORKDIR /app

RUN apt-get update && apt-get install -y cron

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "main.py"]