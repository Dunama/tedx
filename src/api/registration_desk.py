from flask import Blueprint, jsonify, session, request
from sqlalchemy import or_
from src.db.models.events import Event
from src.db.models.attendees import Attendee
from src.models import db

registration_bp = Blueprint('registration', __name__, url_prefix='/registration')

@registration_bp.route('/validate', methods=['POST'])
def validate_ticket():
    """Validate ticket by serial number and/or name"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Normalize inputs to lowercase for consistent matching
        serial = data.get('ticket_serial', '').strip().lower()
        name = data.get('attendee_name', '').strip().lower()
        
        if not serial and not name:
            return jsonify({'error': 'Either serial number or attendee name is required'}), 400
        
        # Find attendee by name and/or serial (both inputs are now lowercase)
        attendee = Event.find_by_name_or_serial(name=name, serial=serial)
        
        if not attendee:
            return jsonify({
                'status': 'invalid',
                'message': 'Attendee not found. Please verify the serial number and name.'
            }), 404
        
        # Check if name matches (if provided) - both names converted to lowercase for comparison
        if name and attendee.name.lower() != name:
            return jsonify({
                'status': 'invalid', 
                'message': f'Name mismatch. Expected: {attendee.name}'
            }), 400
        
        # Check if already checked in
        if attendee.checked_in:
            return jsonify({
                'status': 'already_checked_in',
                'message': f'{attendee.name} is already checked in at {attendee.checked_in_time}',
                'attendee': {
                    'name': attendee.name,
                    'email': attendee.email,
                    'event_id': attendee.event_id,
                    'location': attendee.location,
                    'checked_in': True,
                    'checked_in_time': attendee.checked_in_time.isoformat() if attendee.checked_in_time else None
                }
            }), 200
        
        # Check in the attendee
        attendee.check_in_attendee()
        
        return jsonify({
            'status': 'success',
            'message': f'{attendee.name} checked in successfully!',
            'attendee': {
                'name': attendee.name,
                'email': attendee.email, 
                'event_id': attendee.event_id,
                'location': attendee.location,
                'checked_in': True,
                'checked_in_time': attendee.checked_in_time.isoformat() if attendee.checked_in_time else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@registration_bp.route('/search', methods=['GET'])
def search_attendees():
    """Search attendees by name for autocomplete - enhanced with better matching"""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify({'attendees': []})

    try:
        query_lower = query.lower()
        
        # First priority: exact name matches (case insensitive)
        exact_matches = Event.query.filter(
            Event.name.ilike(query)
        ).limit(3).all()
        
        # Second priority: names starting with the query
        starts_with_matches = Event.query.filter(
            Event.name.ilike(f'{query}%')
        ).filter(~Event.name.ilike(query)).limit(4).all()
        
        # Third priority: names containing the query
        contains_matches = Event.query.filter(
            Event.name.ilike(f'%{query}%')
        ).filter(
            ~Event.name.ilike(query),
            ~Event.name.ilike(f'{query}%')
        ).limit(3).all()
        
        # Fourth priority: event_id matches
        event_id_matches = Event.query.filter(
            Event.event_id.ilike(f'%{query}%')
        ).limit(3).all()
        
        # Combine all results, removing duplicates
        all_matches = []
        seen_ids = set()
        
        for match_list in [exact_matches, starts_with_matches, contains_matches, event_id_matches]:
            for attendee in match_list:
                if attendee.id not in seen_ids:
                    all_matches.append(attendee)
                    seen_ids.add(attendee.id)
                    if len(all_matches) >= 10:  # Limit to 10 results
                        break
            if len(all_matches) >= 10:
                break
        
        results = [{
            'id': a.id, 
            'name': a.name, 
            'email': a.email,
            'event_id': a.event_id,
            'checked_in': a.checked_in
        } for a in all_matches]
        
        return jsonify({'attendees': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@registration_bp.route('/stats', methods=['GET'])
def get_registration_stats():
    """Get real-time registration statistics"""
    try:
        total_registered = Event.get_total_registered()
        checked_in = Event.get_checked_in_attendees()
        event_capacity = Event.get_event_capacity()
        checkin_rate = Event.get_checked_in_rate()
        
        return jsonify({
            'total_registered': total_registered,
            'checked_in': checked_in,
            'event_capacity': event_capacity,
            'checkin_rate': checkin_rate
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
