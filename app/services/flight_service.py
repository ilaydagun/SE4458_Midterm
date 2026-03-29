from app.models.flight import Flight
from app.extensions import db
from app.utils.helpers import parse_datetime


def create_flight(data):
    flight_number = str(data.get("flight_number", "")).strip()
    airport_from = str(data.get("airport_from", "")).strip()
    airport_to = str(data.get("airport_to", "")).strip()

    date_from = parse_datetime(data.get("date_from"))
    date_to = parse_datetime(data.get("date_to"))

    try:
        duration = int(data.get("duration"))
        capacity = int(data.get("capacity"))
    except (TypeError, ValueError):
        return None, "Duration and capacity must be integers"

    if not flight_number:
        return None, "Flight number is required"

    if not airport_from or not airport_to:
        return None, "Airport from and airport to are required"

    if not date_from or not date_to:
        return None, "Invalid date format. Use ISO format like 2026-04-01T09:00:00"

    if date_to <= date_from:
        return None, "date_to must be later than date_from"

    if duration <= 0:
        return None, "Duration must be greater than 0"

    if capacity <= 0:
        return None, "Capacity must be greater than 0"

    duplicate_flight = Flight.query.filter_by(
        flight_number=flight_number,
        date_from=date_from
    ).first()

    if duplicate_flight:
        return None, "A flight with the same flight number and departure date already exists"

    flight = Flight(
        flight_number=flight_number,
        date_from=date_from,
        date_to=date_to,
        airport_from=airport_from,
        airport_to=airport_to,
        duration=duration,
        capacity=capacity
    )

    db.session.add(flight)
    db.session.commit()

    return flight, None


def get_flight_by_number_and_date(flight_number, date_value):
    parsed_date = parse_datetime(date_value)
    if not parsed_date:
        return None

    return Flight.query.filter_by(
        flight_number=str(flight_number).strip(),
        date_from=parsed_date
    ).first()


def query_flights(filters):
    query = Flight.query

    airport_from = filters.get("airport_from")
    airport_to = filters.get("airport_to")
    date_from = parse_datetime(filters.get("date_from")) if filters.get("date_from") else None
    date_to = parse_datetime(filters.get("date_to")) if filters.get("date_to") else None

    try:
        number_of_people = int(filters.get("number_of_people", 1))
    except (TypeError, ValueError):
        number_of_people = 1

    if number_of_people <= 0:
        number_of_people = 1

    if airport_from:
        query = query.filter(Flight.airport_from.ilike(f"%{airport_from.strip()}%"))

    if airport_to:
        query = query.filter(Flight.airport_to.ilike(f"%{airport_to.strip()}%"))

    if date_from:
        query = query.filter(Flight.date_from >= date_from)

    if date_to:
        query = query.filter(Flight.date_to <= date_to)

    all_results = query.order_by(Flight.date_from.asc()).all()

    available_results = []
    for flight in all_results:
        available_seats = flight.capacity - len(flight.tickets)
        if available_seats >= number_of_people:
            available_results.append(flight)

    return available_results