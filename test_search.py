from app import app, db
from src.db.models.events import Event

with app.app_context():
    # Test the search functionality that the autocomplete uses
    print("Testing search functionality:")
    
    # Test search for "Usama" (partial name)
    search_results = Event.query.filter(Event.name.ilike('%Usama%')).limit(10).all()
    print(f"\nSearch results for 'Usama': {len(search_results)} found")
    for result in search_results:
        print(f"  - {result.name} ({result.event_id})")
    
    # Test search for "Ibrahim" (partial name)
    search_results2 = Event.query.filter(Event.name.ilike('%Ibrahim%')).limit(10).all()
    print(f"\nSearch results for 'Ibrahim': {len(search_results2)} found")
    for result in search_results2:
        print(f"  - {result.name} ({result.event_id})")
        
    # Test search for "Ahmed" (partial name)
    search_results3 = Event.query.filter(Event.name.ilike('%Ahmed%')).limit(10).all()
    print(f"\nSearch results for 'Ahmed': {len(search_results3)} found")
    for result in search_results3:
        print(f"  - {result.name} ({result.event_id})")
