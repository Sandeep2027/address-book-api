# Address Book API

FastAPI-based REST API for managing addresses with latitude/longitude coordinates.  
Supports full CRUD and proximity (nearby) search using the Haversine formula + bounding-box optimization.

## Features
- Create, Read, Update, Delete addresses  
- Coordinate validation (latitude/longitude ranges)  
- Nearby search within specified distance (km)  
- SQLite database (file: `addressbook.db`)  
- Auto-generated interactive docs (Swagger UI)

## Tech Stack
- Python 3.8+
- FastAPI
- Pydantic (validation & serialization)
- SQLite (via built-in `sqlite3`)

## Project Structure