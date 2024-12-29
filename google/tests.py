import pyproj

def getPoints():
    start = (13.050217, 77.619350)  # New York City
    destination = (13.050896, 77.619439 )  # London

    geod = pyproj.Geod(ellps='WGS84')
    distance_km, bearing, _ = geod.inv(start[1], start[0], destination[1], destination[0])

    interval_km = distance_km / 10.0

    current_distance = 0
    points = []
    while current_distance <= distance_km:
        lat, lon, _ = geod.fwd(start[1], start[0], bearing, current_distance)
        points.append((lat, lon))
        current_distance += interval_km

    return points


