from src.models import db

class Attendee(db.Model):
    __tablename__ = 'attendees'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    location = db.Column(db.String(200))

    def __repr__(self):
        return f"<Attendee {self.name} - {self.email}>"

# Function to migrate static attendees list to database
def migrate_attendees(attendees_list):
    for attendee_data in attendees_list:
        existing = Attendee.query.filter_by(email=attendee_data['email']).first()
        if not existing:
            attendee = Attendee(
                event_id=attendee_data.get('event_id', ''),
                name=attendee_data.get('name', ''),
                email=attendee_data.get('email', ''),
                location=attendee_data.get('Location', '')
            )
            db.session.add(attendee)
    db.session.commit()
