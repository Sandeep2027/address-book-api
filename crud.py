import math

from sqlite3 import Connection

from schemas import AddressCreate, Address

def create_address(db: Connection, address: AddressCreate) -> Address:
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO addresses (name, street, city, state, zip_code, latitude, longitude)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (address.name, address.street, address.city, address.state, address.zip_code, address.latitude, address.longitude))
    db.commit()
    return Address(id=cursor.lastrowid, **address.dict())

def get_address(db: Connection, address_id: int) -> Address | None:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM addresses WHERE id = ?", (address_id,))
    row = cursor.fetchone()
    if row is None:
        return None
    return Address(**dict(row))

def update_address(db: Connection, address_id: int, address: AddressCreate) -> Address | None:
    cursor = db.cursor()
    cursor.execute("""
    UPDATE addresses
    SET name = ?, street = ?, city = ?, state = ?, zip_code = ?, latitude = ?, longitude = ?
    WHERE id = ?
    """, (address.name, address.street, address.city, address.state, address.zip_code, address.latitude, address.longitude, address_id))
    db.commit()
    if cursor.rowcount == 0:
        return None
    return Address(id=address_id, **address.dict())

def delete_address(db: Connection, address_id: int) -> Address | None:
    addr = get_address(db, address_id)
    if addr is None:
        return None
    cursor = db.cursor()
    cursor.execute("DELETE FROM addresses WHERE id = ?", (address_id,))
    db.commit()
    return addr

def get_addresses_nearby(db: Connection, lat: float, lon: float, distance: float) -> list[Address]:
    r = 6371
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    d_lat = distance / r
    d_lon = d_lat / math.cos(lat_rad) if math.cos(lat_rad) != 0 else float('inf')
    min_lat = lat - math.degrees(d_lat)
    max_lat = lat + math.degrees(d_lat)
    min_lon = lon - math.degrees(d_lon)
    max_lon = lon + math.degrees(d_lon)
    cursor = db.cursor()
    cursor.execute("""
    SELECT * FROM addresses
    WHERE latitude >= ? AND latitude <= ? AND longitude >= ? AND longitude <= ?
    """, (min_lat, max_lat, min_lon, max_lon))
    candidates = cursor.fetchall()
    nearby = []
    for row in candidates:
        dist = haversine(lon, lat, row['longitude'], row['latitude'])
        if dist <= distance:
            nearby.append(Address(**dict(row)))
    return nearby

def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371
    return c * r