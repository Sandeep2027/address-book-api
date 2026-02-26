from pydantic import BaseModel, validator

class AddressBase(BaseModel):
    name: str
    street: str
    city: str
    state: str
    zip_code: str
    latitude: float
    longitude: float

    @validator('latitude')
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int