from app.extensions import db


class Flight(db.Model):
    __tablename__ = "flights"

    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(50), nullable=False)

    date_from = db.Column(db.DateTime, nullable=False)
    date_to = db.Column(db.DateTime, nullable=False)

    airport_from = db.Column(db.String(100), nullable=False)
    airport_to = db.Column(db.String(100), nullable=False)

    duration = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    tickets = db.relationship("Ticket", backref="flight", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "flight_number": self.flight_number,
            "date_from": self.date_from.isoformat() if self.date_from else None,
            "date_to": self.date_to.isoformat() if self.date_to else None,
            "airport_from": self.airport_from,
            "airport_to": self.airport_to,
            "duration": self.duration,
            "capacity": self.capacity,
            "available_seats": self.capacity - len(self.tickets)
        }