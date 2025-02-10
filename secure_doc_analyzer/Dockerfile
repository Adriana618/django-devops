FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "secure_doc_analyzer.wsgi:application", "--bind", "0.0.0.0:8000"]