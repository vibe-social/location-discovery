import pandas as pd


def reverse_geocode(database: pd.DataFrame, latitude: float, longitude: float) -> str:
    """
    Convert geographic coordinates (latitude and longitude) to an IP address.

    Args:
        database (DataFrame): IP2Location database
        latitude (float): Latitude to reverse geocode.
        longitude (float): Longitude to reverse geocode.

    Returns:
        str: The IP address of the geographic coordinates.
    """
    # TODO
    return "123.456.789.0"
