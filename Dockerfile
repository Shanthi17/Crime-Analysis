# start by pulling the python image
FROM python:3.11.3

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .

EXPOSE 8080

CMD ["python", "app.py"]

