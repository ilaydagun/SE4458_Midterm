from app.models.ticket import Ticket
from app.models.checkin import CheckIn
from app.extensions import db
from app.services.flight_service import get_flight_by_number_and_date
from app.utils.seat_generator import generate_next_seat


def perform_checkin(flight_number, date_value, passenger_name):
    flight = get_flight_by_number_and_date(flight_number, date_value)

    if not flight:
        return None, "Flight not found"

    cleaned_name = str(passenger_name).strip()

    if not cleaned_name:
        return None, "Passenger name is required"

    ticket = Ticket.query.filter_by(
        flight_id=flight.id,
        passenger_name=cleaned_name
    ).first()

    if not ticket:
        return None, "Ticket not found"

    if ticket.is_checked_in:
        return None, "Passenger already checked in"

    used_seats_count = CheckIn.query.join(Ticket).filter(Ticket.flight_id == flight.id).count()
    seat_number = generate_next_seat(used_seats_count)

    ticket.is_checked_in = True
    ticket.seat_number = seat_number

    checkin = CheckIn(
        ticket_id=ticket.id,
        seat_number=seat_number
    )

    db.session.add(checkin)
    db.session.commit()

    return {
        "ticket_id": ticket.id,
        "passenger_name": ticket.passenger_name,
        "seat_number": seat_number
    }, None