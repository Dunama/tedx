from flask import Blueprint, jsonify, request, current_app, session
from src.db.models.tickets import Ticket
from src.models import db
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps

tickets_bp = Blueprint('tickets', __name__, url_prefix='/api/tickets')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@tickets_bp.route('/purchase', methods=['POST'])
@login_required
def purchase_ticket():
    """Purchase a new ticket"""
    try:
        data = request.get_json()
        required_fields = ['ticket_type', 'quantity', 'price']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        user_id = session['user']['id']
        ticket = Ticket.create_ticket(
            user_id=user_id,
            ticket_type=data['ticket_type'],
            quantity=data['quantity'],
            price=data['price']
        )
        
        return jsonify({
            'message': 'Ticket purchased successfully',
            'ticket': ticket.to_dict()
        }), 201

    except SQLAlchemyError as e:
        current_app.logger.error(f"Error purchasing ticket: {str(e)}")
        return jsonify({'error': 'Failed to purchase ticket'}), 500

@tickets_bp.route('/my-tickets', methods=['GET'])
@login_required
def get_my_tickets():
    """Get all tickets for the logged-in user"""
    try:
        user_id = session['user']['id']
        tickets = Ticket.get_user_tickets(user_id)
        return jsonify({
            'tickets': [ticket.to_dict() for ticket in tickets]
        }), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"Error fetching tickets: {str(e)}")
        return jsonify({'error': 'Failed to fetch tickets'}), 500

@tickets_bp.route('/validate', methods=['POST'])
@login_required
def validate_ticket():
    """Validate and mark a ticket as used"""
    try:
        data = request.get_json()
        if not data or 'ticket_id' not in data or 'device_id' not in data:
            return jsonify({'error': 'Missing ticket_id or device_id'}), 400

        ticket = Ticket.query.get(data['ticket_id'])
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404

        if ticket.is_used:
            return jsonify({'error': 'Ticket already used'}), 400

        success = ticket.mark_as_used(data['device_id'])
        if success:
            return jsonify({
                'message': 'Ticket validated successfully',
                'ticket': ticket.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Failed to validate ticket'}), 400

    except SQLAlchemyError as e:
        current_app.logger.error(f"Error validating ticket: {str(e)}")
        return jsonify({'error': 'Failed to validate ticket'}), 500

@tickets_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """Get ticket statistics"""
    try:
        stats = Ticket.get_ticket_stats()
        return jsonify(stats), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({'error': 'Failed to fetch statistics'}), 500

@tickets_bp.route('/device-usage/<device_id>', methods=['GET'])
@login_required
def get_device_usage(device_id):
    """Get ticket usage statistics for a specific device"""
    try:
        usage_count = Ticket.get_device_usage(device_id)
        return jsonify({
            'device_id': device_id,
            'tickets_validated': usage_count
        }), 200

    except SQLAlchemyError as e:
        current_app.logger.error(f"Error fetching device usage: {str(e)}")
        return jsonify({'error': 'Failed to fetch device usage'}), 500 