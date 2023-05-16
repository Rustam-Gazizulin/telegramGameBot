FROM python:3.10-slim

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["python",  "main.py"]