def convert_coordinates(coords):
    # Separate the string into latitude, latitude direction, longitude, and longitude direction
    lat, lat_dir, lon, lon_dir = coords.split()

    # Convert the latitude and longitude to float
    lat = float(lat)
    lon = float(lon)

    # Convert the direction into positive or negative based on the cardinal direction
    if lat_dir == 'S':
        lat = -lat
    if lon_dir == 'W':
        lon = -lon

    # Return the coordinates in tuple form
    return lat, lon

# Test the function
coords = "37.7749 N 122.4194 W"
lat, lon = convert_coordinates(coords)
print(f"Latitude: {lat}, Longitude: {lon}")  # Output: Latitude: 37.7749, Longitude: -122.4194