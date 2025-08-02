import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import app
from src.db.models.attendees import Attendee, migrate_attendees

# The static attendees list copied from src/db/models/attendees.py (original static list)
attendees_list = [
  {
    "event_id": "gst-SHoKlPKV5U1wI9j",
    "name": "Usama Abdulhamid Kambari",
    "email": "abdulhamidusamakambari@gmail.com",
    "Location": "Sengere futy"
  },
  {
    "event_id": "gst-5ezcWzcqJto89jz",
    "name": "Abdullahi Muhammed",
    "email": "abdullahimuhammed7195@gmail.com",
    "Location": "Yola, Adamawa state."
  },
  # ... (rest of the attendees)
]

with app.app_context():
    migrate_attendees(attendees_list)
    print("Attendees migrated successfully.")
