import os
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.extensions import limiter
from app.services.flight_service import create_flight, query_flights, get_flight_by_number_and_date
from app.services.file_service import import_flights_from_csv
from app.models.ticket import Ticket
from app.utils.helpers import success_response, error_response
from app.utils.pagination import paginate_query
from app.utils.rate_limit import QUERY_FLIGHT_LIMIT

flight_bp = Blueprint("flight", __name__)


@flight_bp.route("/", methods=["POST"])
@jwt_required()
def add_flight():
    """
    Add a new flight
    ---
    tags:
      - Flights
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
            date_from:
              type: string
              example: 2026-04-01T09:00:00
            date_to:
              type: string
              example: 2026-04-01T11:00:00
            airport_from:
              type: string
              example: Izmir
            airport_to:
              type: string
              example: Istanbul
            duration:
              type: integer
              example: 120
            capacity:
              type: integer
              example: 50
          required:
            - flight_number
            - date_from
            - date_to
            - airport_from
            - airport_to
            - duration
            - capacity
    responses:
      201:
        description: Flight added successfully
      400:
        description: Invalid input
      401:
        description: Unauthorized
    """
    data = request.get_json() or {}
    flight, error = create_flight(data)

    if error:
        return error_response(error, 400)

    return success_response("Flight added successfully", flight.to_dict(), 201)


@flight_bp.route("/upload", methods=["POST"])
@jwt_required()
def add_flight_by_file():
    """
    Upload flight CSV
    ---
    tags:
      - Flights
    consumes:
      - multipart/form-data
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
      - name: file
        in: formData
        type: file
        required: true
        description: CSV file
    responses:
      200:
        description: File processed successfully
      400:
        description: File missing or invalid
      401:
        description: Unauthorized
    """
    if "file" not in request.files:
        return error_response("CSV file is required", 400)

    file = request.files["file"]

    if file.filename == "":
        return error_response("No file selected", 400)

    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    result = import_flights_from_csv(file_path)
    return success_response("File processed successfully", result, 200)


@flight_bp.route("/query", methods=["GET"])
#@limiter.limit(QUERY_FLIGHT_LIMIT)
def query_flight():
    """
    Query available flights
    ---
    tags:
      - Flights
    parameters:
      - name: date_from
        in: query
        type: string
        required: false
        example: 2026-04-01T00:00:00
      - name: date_to
        in: query
        type: string
        required: false
        example: 2026-04-30T23:59:59
      - name: airport_from
        in: query
        type: string
        required: false
        example: Izmir
      - name: airport_to
        in: query
        type: string
        required: false
        example: Istanbul
      - name: number_of_people
        in: query
        type: integer
        required: false
        example: 2
      - name: trip_type
        in: query
        type: string
        required: false
        example: one_way
      - name: page
        in: query
        type: integer
        required: false
        default: 1
      - name: per_page
        in: query
        type: integer
        required: false
        default: 10
    responses:
      200:
        description: Flights fetched successfully
      429:
        description: Rate limit exceeded
    """
    filters = request.args.to_dict()

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
    except ValueError:
        return error_response("page and per_page must be integers", 400)

    if page <= 0 or per_page <= 0:
        return error_response("page and per_page must be greater than 0", 400)

    flights = query_flights(filters)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_items = flights[start:end]

    return success_response(
        "Flights fetched successfully",
        {
            "items": [flight.to_dict() for flight in paginated_items],
            "page": page,
            "per_page": per_page,
            "total": len(flights),
            "pages": (len(flights) + per_page - 1) // per_page
        },
        200
    )


@flight_bp.route("/passengers", methods=["GET"])
@jwt_required()
def query_flight_passenger_list():
    """
    Query passenger list for a flight
    ---
    tags:
      - Flights
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token
      - name: flight_number
        in: query
        type: string
        required: true
        example: TK101
      - name: date
        in: query
        type: string
        required: true
        example: 2026-04-01T09:00:00
      - name: page
        in: query
        type: integer
        required: false
        default: 1
      - name: per_page
        in: query
        type: integer
        required: false
        default: 10
    responses:
      200:
        description: Passenger list fetched successfully
      400:
        description: Missing parameters
      401:
        description: Unauthorized
      404:
        description: Flight not found
    """
    flight_number = request.args.get("flight_number")
    date_value = request.args.get("date")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    if not flight_number or not date_value:
        return error_response("flight_number and date are required", 400)

    flight = get_flight_by_number_and_date(flight_number, date_value)

    if not flight:
        return error_response("Flight not found", 404)

    ticket_query = Ticket.query.filter_by(flight_id=flight.id)
    paginated_data = paginate_query(ticket_query, page, per_page)

    return success_response("Passenger list fetched successfully", paginated_data, 200)