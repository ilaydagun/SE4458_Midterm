from datetime import datetime


def parse_datetime(value):
    if not value:
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def success_response(message, data=None, status_code=200):
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response, status_code


def error_response(message, status_code=400):
    return {
        "success": False,
        "message": message
    }, status_code