from flask import Blueprint, request
from app.services.checkin_service import perform_checkin
from app.utils.helpers import success_response, error_response

checkin_bp = Blueprint("checkin", __name__)


@checkin_bp.route("/", methods=["POST"])
def check_in():
    """
    Check in passenger
    ---
    tags:
      - CheckIn
    consumes:
      - application/json
    parameters:
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
            passenger_name:
              type: string
              example: Ilayda Gun
          required:
            - flight_number
            - date
            - passenger_name
    responses:
      200:
        description: Check-in completed successfully
      400:
        description: Invalid request
    """
    data = request.get_json() or {}

    flight_number = data.get("flight_number")
    date_value = data.get("date")
    passenger_name = data.get("passenger_name")

    if not flight_number or not date_value or not passenger_name:
        return error_response("flight_number, date and passenger_name are required", 400)

    result, error = perform_checkin(flight_number, date_value, passenger_name)

    if error:
        return error_response(error, 400)

    return success_response("Check-in completed successfully", result, 200)