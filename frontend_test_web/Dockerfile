FROM python:3.12-alpine
WORKDIR /Frontend
COPY . .
ENTRYPOINT ["python", "-m", "http.server", "3000", "--bind", "0.0.0.0"]