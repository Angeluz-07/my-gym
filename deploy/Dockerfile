FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean

COPY deploy/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./django-app /app

 
# Run Django’s development server
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

# El contenedor arranca ejecutando el entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]