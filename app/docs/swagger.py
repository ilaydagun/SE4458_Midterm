swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Airline Ticketing API",
        "description": "API for airline ticketing system",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": [
        "http"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}