# Dockerfile example
FROM python:3.9-alpine

COPY . ./backend

WORKDIR backend

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 81

CMD ["python", "main.py"]

