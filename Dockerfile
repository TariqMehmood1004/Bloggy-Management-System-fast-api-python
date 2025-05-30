# Use official Python image with version 3.12.10
FROM python:3.12.10-slim


WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "blog_fast_api_python.main:app", "--host", "0.0.0.0", "--port", "8000"]
