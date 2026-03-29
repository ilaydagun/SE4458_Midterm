FLIGHT_CREATE_SCHEMA = {
    "type": "object",
    "required": [
        "flight_number",
        "date_from",
        "date_to",
        "airport_from",
        "airport_to",
        "duration",
        "capacity"
    ],
    "properties": {
        "flight_number": {"type": "string", "example": "TK101"},
        "date_from": {"type": "string", "example": "2026-04-01T09:00:00"},
        "date_to": {"type": "string", "example": "2026-04-01T11:00:00"},
        "airport_from": {"type": "string", "example": "Izmir"},
        "airport_to": {"type": "string", "example": "Istanbul"},
        "duration": {"type": "integer", "example": 120},
        "capacity": {"type": "integer", "example": 50}
    }
}

FLIGHT_QUERY_SCHEMA = {
    "type": "object",
    "properties": {
        "date_from": {"type": "string", "example": "2026-04-01T00:00:00"},
        "date_to": {"type": "string", "example": "2026-04-30T23:59:59"},
        "airport_from": {"type": "string", "example": "Izmir"},
        "airport_to": {"type": "string", "example": "Istanbul"},
        "number_of_people": {"type": "integer", "example": 2},
        "trip_type": {"type": "string", "example": "one_way"}
    }
}