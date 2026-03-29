from app.models.ticket import Ticket
from app.extensions import db
from app.services.flight_service import get_flight_by_number_and_date


def buy_ticket(flight_number, date_value, passenger_names):
    flight = get_flight_by_number_and_date(flight_number, date_value)

    if not flight:
        return None, "Flight not found"

    if not isinstance(passenger_names, list) or len(passenger_names) == 0:
        return None, "passenger_names must be a non-empty list"

    cleaned_names = []
    seen_names = set()

    for name in passenger_names:
        cleaned_name = str(name).strip()

        if not cleaned_name:
            return None, "Passenger names cannot be empty"

        if cleaned_name.lower() in seen_names:
            return None, "Duplicate passenger names are not allowed in the same purchase"

        existing_ticket = Ticket.query.filter_by(
            flight_id=flight.id,
            passenger_name=cleaned_name
        ).first()

        if existing_ticket:
            return None, f"Passenger '{cleaned_name}' already has a ticket for this flight"

        seen_names.add(cleaned_name.lower())
        cleaned_names.append(cleaned_name)

    available_seats = flight.capacity - len(flight.tickets)

    if available_seats < len(cleaned_names):
        return None, "Sold out or insufficient seats"

    created_tickets = []

    for passenger_name in cleaned_names:
        ticket = Ticket(
            flight_id=flight.id,
            passenger_name=passenger_name
        )
        db.session.add(ticket)
        created_tickets.append(ticket)

    db.session.commit()

    return created_tickets, None