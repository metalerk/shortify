FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]