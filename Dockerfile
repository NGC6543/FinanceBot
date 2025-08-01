FROM python:3.11.0

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY handlers ./handlers
COPY /*.py .
COPY *.sql .

CMD ["python", "main_finance.py"]