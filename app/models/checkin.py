from app.extensions import db


class CheckIn(db.Model):
    __tablename__ = "checkins"

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("tickets.id"), nullable=False, unique=True)
    seat_number = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "seat_number": self.seat_number
        }