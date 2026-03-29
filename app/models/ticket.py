from app.extensions import db


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)
    passenger_name = db.Column(db.String(120), nullable=False)
    seat_number = db.Column(db.String(10), nullable=True)
    is_checked_in = db.Column(db.Boolean, default=False, nullable=False)

    checkin = db.relationship("CheckIn", backref="ticket", uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "flight_id": self.flight_id,
            "passenger_name": self.passenger_name,
            "seat_number": self.seat_number,
            "is_checked_in": self.is_checked_in
        }