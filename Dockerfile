FROM python:3.8-slim-buster
WORKDIR /app
EXPOSE 5000
COPY . .
RUN pip install -r requirements.txt
CMD export FLASK_ENV=development && flask run --port=5000 --host=0.0.0.0
