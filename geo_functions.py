from geopy.geocoders import Nominatim

def get_address_from_lat_lng(latitude, longitude):
    # Initialize the Nominatim geocoder
    geolocator = Nominatim(user_agent="reverse_geocoding_example")

    try:
        # Perform reverse geocoding
        location = geolocator.reverse((latitude, longitude), language="en")
        
        # Extract and return the address
        if location:
            return location.address
        else:
            return "Address not found"

    except Exception as e:
        return f"Error: {str(e)}"

import math

def haversine3d(lat1, lon1, elev1, lat2, lon2, elev2):
    # Radius of the Earth in meters
    earth_radius = 6371000  # Approximate value for average radius
    
    # Convert latitudes and longitudes from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # Calculate differences in latitude, longitude, and elevation
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    delev = elev2 - elev1
    
    # Calculate the distance using the Haversine formula
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c
    
    # Add the difference in elevation (altitude)
    distance += abs(delev)
    
    return "{:.{}f}".format(distance/1000, 4)

def haversine2d(lat1, lon1, lat2, lon2):
    # Radius of the Earth in meters
    earth_radius = 6371000  # Approximate value for average radius
    
    # Convert latitudes and longitudes from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # Calculate differences in latitude and longitude
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Calculate the distance using the Haversine formula
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c
    
    return "{:.{}f}".format(distance/1000, 4)

# Example usage:
lat1 = 12.786699  # Latitude of location 1 (in degrees)
lon1 = 80.21434  # Longitude of location 1 (in degrees)
elev1 = 0  # Altitude of location 1 (in meters)

lat2 = 12.751111330128522  # Latitude of location 2 (in degrees)
lon2 = 80.1970245675958  # Longitude of location 2 (in degrees)
elev2 = 5000  # Altitude of location 2 (in meters)

distance3d = haversine3d(lat1, lon1, elev1, lat2, lon2, elev2)
print("Distance - 3D: ", distance3d, "kms")
distance2d = haversine2d(lat1, lon1, lat2, lon2)
print("Distance - 2D: ", distance2d, "kms")
'''
# Example usage:
latitude = 12.7756  # Replace with the latitude of the region
longitude = 80.75980  # Replace with the longitude of the region

address = get_address_from_lat_lng(latitude, longitude)
print("Address:", address)

'''