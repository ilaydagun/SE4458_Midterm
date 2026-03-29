BUY_TICKET_SCHEMA = {
    "type": "object",
    "required": ["flight_number", "date", "passenger_names"],
    "properties": {
        "flight_number": {"type": "string", "example": "TK101"},
        "date": {"type": "string", "example": "2026-04-01T09:00:00"},
        "passenger_names": {
            "type": "array",
            "items": {"type": "string"},
            "example": ["Ilayda Gun", "Ali Veli"]
        }
    }
}