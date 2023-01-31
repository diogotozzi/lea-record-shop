FROM python:3.11.1-alpine3.17
WORKDIR /sanic
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "server.py"]
