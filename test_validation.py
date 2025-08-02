from app import app, db
from src.db.models.events import Event

with app.app_context():
    # Show first 5 attendees for testing
    attendees = Event.query.limit(5).all()
    print('First 5 attendees for testing:')
    for i, attendee in enumerate(attendees, 1):
        print(f'{i}. Name: "{attendee.name}" | Event ID: {attendee.event_id} | Checked in: {attendee.checked_in}')
    
    # Test the find_by_name_or_serial method
    print('\nTesting name search:')
    test_result = Event.find_by_name_or_serial(name="Usama Abdulhamid Kambari")
    if test_result:
        print(f"Found: {test_result.name} - {test_result.event_id}")
    else:
        print("Not found with exact name")
    
    # Test partial name search
    test_result2 = Event.find_by_name_or_serial(name="Usama")
    if test_result2:
        print(f"Found with partial name: {test_result2.name} - {test_result2.event_id}")
    else:
        print("Not found with partial name")
