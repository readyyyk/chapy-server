FROM python:3.12.7-slim-bullseye

ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]