FROM python:3.11.0

WORKDIR /app

ENV API_TOKEN=""
ENV DBNAME=""
ENV HOST=""
ENV USER=""
ENV PASSWORD=""
ENV PORT=5432

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir
RUN apt install postgresql

COPY handlers ./handlers
COPY /*.py .
COPY *.sql .

CMD ["python", "main_finance.py"]