FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN --mount=type=secret,id=IP_2_LOCATION_TOKEN \
    export IP_2_LOCATION_TOKEN=$(cat /run/secrets/IP_2_LOCATION_TOKEN)

RUN python3 ip2location/download.py

EXPOSE 8080

CMD ["python", "app.py"]
