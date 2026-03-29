import csv
from app.services.flight_service import create_flight


def import_flights_from_csv(file_path):
    imported_count = 0
    errors = []

    with open(file_path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        required_columns = {
            "flight_number",
            "date_from",
            "date_to",
            "airport_from",
            "airport_to",
            "duration",
            "capacity"
        }

        if not reader.fieldnames or not required_columns.issubset(set(reader.fieldnames)):
            return {
                "imported_count": 0,
                "errors": [
                    {
                        "row": 0,
                        "error": "CSV file is missing one or more required columns"
                    }
                ]
            }

        for index, row in enumerate(reader, start=2):
            flight_data = {
                "flight_number": row.get("flight_number"),
                "date_from": row.get("date_from"),
                "date_to": row.get("date_to"),
                "airport_from": row.get("airport_from"),
                "airport_to": row.get("airport_to"),
                "duration": row.get("duration"),
                "capacity": row.get("capacity")
            }

            flight, error = create_flight(flight_data)

            if error:
                errors.append({
                    "row": index,
                    "error": error
                })
            else:
                imported_count += 1

    return {
        "imported_count": imported_count,
        "errors": errors
    }