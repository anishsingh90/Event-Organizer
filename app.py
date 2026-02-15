from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import datetime, timedelta
from models import db, User, Event, Booking
from auth import role_required, get_current_user
from background_tasks import send_booking_confirmation_email, send_event_update_notification

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Initialize database
with app.app_context():
    db.create_all()

# ==================== Authentication Endpoints ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'password', 'name', 'role']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if data['role'] not in ['organizer', 'customer']:
        return jsonify({'error': 'Invalid role. Must be organizer or customer'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User(email=data['email'], name=data['name'], role=data['role'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(
        identity=user.id,
        additional_claims={'role': user.role}
    )
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

# ==================== Event Endpoints (Public) ====================

@app.route('/api/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify({'events': [event.to_dict() for event in events]}), 200

@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify({'event': event.to_dict()}), 200

# ==================== Event Endpoints (Organizer Only) ====================

@app.route('/api/events', methods=['POST'])
@jwt_required()
@role_required('organizer')
def create_event():
    data = request.get_json()
    user = get_current_user()
    
    required_fields = ['title', 'description', 'date', 'location', 'total_tickets', 'price']
    if not all(k in data for k in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        event_date = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
    except:
        return jsonify({'error': 'Invalid date format. Use ISO format'}), 400
    
    event = Event(
        title=data['title'],
        description=data['description'],
        date=event_date,
        location=data['location'],
        total_tickets=data['total_tickets'],
        available_tickets=data['total_tickets'],
        price=data['price'],
        organizer_id=user.id
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({'message': 'Event created successfully', 'event': event.to_dict()}), 201

@app.route('/api/events/<int:event_id>', methods=['PUT'])
@jwt_required()
@role_required('organizer')
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    user = get_current_user()
    
    if event.organizer_id != user.id:
        return jsonify({'error': 'You can only update your own events'}), 403
    
    data = request.get_json()
    
    if 'title' in data:
        event.title = data['title']
    if 'description' in data:
        event.description = data['description']
    if 'date' in data:
        try:
            event.date = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
        except:
            return jsonify({'error': 'Invalid date format'}), 400
    if 'location' in data:
        event.location = data['location']
    if 'price' in data:
        event.price = data['price']
    
    db.session.commit()
    
    # Trigger background task: Notify customers about event update
    bookings = Booking.query.filter_by(event_id=event_id).all()
    if bookings:
        customers = [{'name': b.customer.name, 'email': b.customer.email} for b in bookings]
        send_event_update_notification(event.to_dict(), customers)
    
    return jsonify({'message': 'Event updated successfully', 'event': event.to_dict()}), 200

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
@role_required('organizer')
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    user = get_current_user()
    
    if event.organizer_id != user.id:
        return jsonify({'error': 'You can only delete your own events'}), 403
    
    db.session.delete(event)
    db.session.commit()
    
    return jsonify({'message': 'Event deleted successfully'}), 200

# ==================== Organizer Dashboard ====================

@app.route('/api/organizer/events', methods=['GET'])
@jwt_required()
@role_required('organizer')
def get_organizer_events():
    user = get_current_user()
    events = Event.query.filter_by(organizer_id=user.id).all()
    return jsonify({'events': [event.to_dict() for event in events]}), 200

@app.route('/api/organizer/events/<int:event_id>/bookings', methods=['GET'])
@jwt_required()
@role_required('organizer')
def get_event_bookings(event_id):
    event = Event.query.get_or_404(event_id)
    user = get_current_user()
    
    if event.organizer_id != user.id:
        return jsonify({'error': 'You can only view bookings for your own events'}), 403
    
    bookings = Booking.query.filter_by(event_id=event_id).all()
    return jsonify({'bookings': [booking.to_dict() for booking in bookings]}), 200

# ==================== Booking Endpoints (Customer Only) ====================

@app.route('/api/bookings', methods=['POST'])
@jwt_required()
@role_required('customer')
def create_booking():
    data = request.get_json()
    user = get_current_user()
    
    if not all(k in data for k in ['event_id', 'tickets_count']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    event = Event.query.get_or_404(data['event_id'])
    
    if event.available_tickets < data['tickets_count']:
        return jsonify({'error': 'Not enough tickets available'}), 400
    
    total_price = event.price * data['tickets_count']
    
    booking = Booking(
        event_id=event.id,
        customer_id=user.id,
        tickets_count=data['tickets_count'],
        total_price=total_price
    )
    
    event.available_tickets -= data['tickets_count']
    
    db.session.add(booking)
    db.session.commit()
    
    # Trigger background task: Send booking confirmation email
    booking_data = {
        'customer_name': user.name,
        'customer_email': user.email,
        'event_title': event.title,
        'tickets_count': data['tickets_count'],
        'total_price': total_price,
        'booking_date': booking.booking_date.isoformat()
    }
    send_booking_confirmation_email(booking_data)
    
    return jsonify({'message': 'Booking successful', 'booking': booking.to_dict()}), 201

@app.route('/api/bookings', methods=['GET'])
@jwt_required()
@role_required('customer')
def get_customer_bookings():
    user = get_current_user()
    bookings = Booking.query.filter_by(customer_id=user.id).all()
    return jsonify({'bookings': [booking.to_dict() for booking in bookings]}), 200

# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Event Booking API is running'}), 200

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Event Booking System API")
    print("="*60)
    print("Server running on: http://localhost:5000")
    print("API Documentation: See README.md")
    print("="*60 + "\n")
    app.run(debug=True, port=5000)
