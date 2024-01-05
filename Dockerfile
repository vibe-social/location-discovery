FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN --mount=type=secret,id=IP_2_LOCATION_TOKEN export \
    IP_2_LOCATION_TOKEN=$(cat /run/secrets/IP_2_LOCATION_TOKEN)

RUN python ip2location/download.py

EXPOSE 8080

CMD ["python", "app.py"]
