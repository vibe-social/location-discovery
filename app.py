import os
from dotenv import load_dotenv
from controllers.geocode import geocode
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from ip2location.database import load_database
from controllers.distance import calculate_distance
from controllers.reverse_geocode import reverse_geocode


# Load the IP2Location database and export it to a global variable
database = load_database()
globals()["database"] = database

# Define the Flask app and the API
app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Location Discovery API",
    description="API for location discovery",
    doc="/openapi",
)

# Read the environment variables
load_dotenv()
LOCATION_DISCOVERY_SERVER_MODE = os.getenv("LOCATION_DISCOVERY_SERVER_MODE", "debug")
LOCATION_DISCOVERY_SERVER_PORT = os.getenv("LOCATION_DISCOVERY_SERVER_PORT", 8080)

# Define the OpenAPI models
geocode_model = api.model(
    "Geocode",
    description="Convert an IP address to geographic coordinates (latitude and longitude).",
    model={
        "address": fields.String(
            required=True, description="IP address to geocode", example="123.456.789.0"
        )
    },
)
reverse_geocode_model = api.model(
    "Reverse Geocode",
    description="Convert geographic coordinates (latitude and longitude) to an IP address.",
    model={
        "latitude": fields.Float(
            required=True, description="Latitude to reverse geocode", example=123.456
        ),
        "longitude": fields.Float(
            required=True, description="Longitude to reverse geocode", example=654.321
        ),
    },
)
distance_model = api.model(
    "Distance",
    description="Calculate the distance between two geographic coordinates (latitude and longitude).",
    model={
        "latitude1": fields.Float(
            required=True,
            description="Latitude of the first location",
            example=123.456,
        ),
        "longitude1": fields.Float(
            required=True,
            description="Longitude of the first location",
            example=654.321,
        ),
        "latitude2": fields.Float(
            required=True,
            description="Latitude of the second location",
            example=123.456,
        ),
        "longitude2": fields.Float(
            required=True,
            description="Longitude of the second location",
            example=654.321,
        ),
    },
)
database_model = api.model(
    "Database",
    description="IP2Location database",
    model={
        "database": fields.String(required=True, description="IP2Location database")
    },
)
health_model = api.model(
    "Health",
    description="Health check",
    model={"status": fields.String(required=True, description="Health status")},
)


# Geocode endpoint
@api.route("/geocode")
class Geocode(Resource):
    @api.expect(geocode_model)
    def post(self):
        data = request.get_json()
        address = data.get("address")

        latitude, longitude = geocode(address)

        return jsonify({"latitude": latitude, "longitude": longitude})


# Reverse geocode endpoint
@api.route("/reverse-geocode")
class ReverseGeocode(Resource):
    @api.expect(reverse_geocode_model)
    def post(self):
        data = request.get_json()
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        address = reverse_geocode(latitude, longitude)

        return jsonify({"address": address})


# Distance endpoint
@api.route("/distance")
class Distance(Resource):
    @api.expect(distance_model)
    def post(self):
        data = request.get_json()
        latitude1 = data.get("latitude1")
        longitude1 = data.get("longitude1")
        latitude2 = data.get("latitude2")
        longitude2 = data.get("longitude2")

        distance = calculate_distance(latitude1, longitude1, latitude2, longitude2)

        return jsonify({"distance": distance})


# Database endpoint
@api.route("/database")
class Database(Resource):
    @api.expect(database_model)
    def get(self):
        # Select random 100 elements from database
        return jsonify(database.sample(n=100).to_json(orient="records"))


# Health check endpoint
@api.route("/health")
class Health(Resource):
    @api.expect(health_model)
    def get(self):
        return {"status": "ok"}


if __name__ == "__main__":
    app.run(
        debug=LOCATION_DISCOVERY_SERVER_MODE == "debug",
        host="0.0.0.0",
        port=LOCATION_DISCOVERY_SERVER_PORT,
    )
