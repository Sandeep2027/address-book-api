import logging
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlite3 import Connection

import crud
import schemas
from database import get_db, init_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Address Book API",
    description="Simple address book with coordinate-based proximity search",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("Database initialized")

@app.post("/addresses/", response_model=schemas.Address, status_code=201)
def create_address(address: schemas.AddressCreate, db: Connection = Depends(get_db)):
    return crud.create_address(db, address)

@app.get("/addresses/{address_id}", response_model=schemas.Address)
def read_address(address_id: int, db: Connection = Depends(get_db)):
    address = crud.get_address(db, address_id)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@app.put("/addresses/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, address: schemas.AddressCreate, db: Connection = Depends(get_db)):
    updated = crud.update_address(db, address_id, address)
    if updated is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return updated

@app.delete("/addresses/{address_id}", response_model=schemas.Address)
def delete_address(address_id: int, db: Connection = Depends(get_db)):
    deleted = crud.delete_address(db, address_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return deleted

@app.get("/addresses/nearby/", response_model=list[schemas.Address])
def get_nearby(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    distance: float = Query(..., gt=0, description="Max distance in kilometers"),
    db: Connection = Depends(get_db)
):
    """Find addresses within the given distance (km) from the coordinates"""
    return crud.get_addresses_nearby(db, lat, lon, distance)