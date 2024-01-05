FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# Set the environment variable
ENV IP_2_LOCATION_TOKEN=$IP_2_LOCATION_TOKEN

RUN python ip2location/download.py

EXPOSE 8080

CMD ["python", "app.py"]
