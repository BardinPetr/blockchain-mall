FROM python:3.9-slim

RUN apt update
RUN apt install -y gcc

WORKDIR backend

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./ ./

EXPOSE 81

CMD ["python", "main.py"]

