from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.ticket_service import buy_ticket
from app.utils.helpers import success_response, error_response

ticket_bp = Blueprint("ticket", __name__)


@ticket_bp.route("/buy", methods=["POST"])
@jwt_required()
def buy():
    """
    Buy ticket
    ---
    tags:
      - Tickets
    consumes:
      - application/json
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            flight_number:
              type: string
              example: TK101
            date:
              type: string
              example: 2026-04-01T09:00:00
            passenger_names:
              type: array
              items:
                type: string
              example:
                - Ilayda Gun
                - Ali Veli
          required:
            - flight_number
            - date
            - passenger_names
    responses:
      201:
        description: Ticket purchased successfully
      400:
        description: Invalid request
      401:
        description: Unauthorized
    """
    data = request.get_json() or {}

    flight_number = data.get("flight_number")
    date_value = data.get("date")
    passenger_names = data.get("passenger_names", [])

    if not flight_number or not date_value or not passenger_names:
        return error_response("flight_number, date and passenger_names are required", 400)

    tickets, error = buy_ticket(flight_number, date_value, passenger_names)

    if error:
        return error_response(error, 400)

    return success_response(
        "Ticket(s) purchased successfully",
        {
            "ticket_numbers": [ticket.id for ticket in tickets],
            "tickets": [ticket.to_dict() for ticket in tickets]
        },
        201
    )