# Quick Start Guide

## Installation & Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the Application**
```bash
python app.py
```

The server will start on `http://localhost:5000`

## Testing the API

### Option 1: Using the Test Script (Recommended)
```bash
python test_api.py
```

This will automatically test all endpoints and show you the background tasks in action.

### Option 2: Using Postman
1. Import `postman_collection.json` into Postman
2. Follow the requests in order
3. Copy the JWT tokens from login responses and use them in subsequent requests

### Option 3: Using curl

#### 1. Register an Organizer
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"organizer@test.com\",\"password\":\"pass123\",\"name\":\"John Doe\",\"role\":\"organizer\"}"
```

#### 2. Register a Customer
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"customer@test.com\",\"password\":\"pass123\",\"name\":\"Jane Doe\",\"role\":\"customer\"}"
```

#### 3. Login as Organizer
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"organizer@test.com\",\"password\":\"pass123\"}"
```

Copy the `access_token` from the response.

#### 4. Create an Event (Replace YOUR_TOKEN)
```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d "{\"title\":\"Music Festival\",\"description\":\"Summer music festival\",\"date\":\"2024-12-31T18:00:00\",\"location\":\"Central Park\",\"total_tickets\":500,\"price\":75.00}"
```

#### 5. Get All Events (No Auth Required)
```bash
curl http://localhost:5000/api/events
```

#### 6. Login as Customer
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"customer@test.com\",\"password\":\"pass123\"}"
```

#### 7. Book Tickets (Replace YOUR_TOKEN and event_id)
```bash
curl -X POST http://localhost:5000/api/bookings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d "{\"event_id\":1,\"tickets_count\":2}"
```

**Watch the console where app.py is running - you'll see the booking confirmation email!**

#### 8. Update Event (Replace YOUR_ORGANIZER_TOKEN)
```bash
curl -X PUT http://localhost:5000/api/events/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ORGANIZER_TOKEN" \
  -d "{\"title\":\"Music Festival - UPDATED\",\"location\":\"Madison Square Garden\"}"
```

**Watch the console - you'll see the event update notification!**

## Background Tasks Demo

The two background tasks will print to the console where `app.py` is running:

1. **Booking Confirmation Email** - Triggered when a customer books tickets
2. **Event Update Notification** - Triggered when an organizer updates an event

Look for these formatted messages in your console:
- 📧 BACKGROUND TASK: Booking Confirmation Email
- 🔔 BACKGROUND TASK: Event Update Notification

## API Endpoints Summary

### Authentication (No Auth Required)
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user

### Events (Public)
- `GET /api/events` - List all events
- `GET /api/events/<id>` - Get event details

### Events (Organizer Only)
- `POST /api/events` - Create event
- `PUT /api/events/<id>` - Update event (triggers notification)
- `DELETE /api/events/<id>` - Delete event
- `GET /api/organizer/events` - Get my events
- `GET /api/organizer/events/<id>/bookings` - Get event bookings

### Bookings (Customer Only)
- `POST /api/bookings` - Book tickets (triggers confirmation email)
- `GET /api/bookings` - Get my bookings

## Video Demo Checklist

When recording your demo video, make sure to show:

1. ✅ Your face (required)
2. ✅ Starting the Flask server
3. ✅ Registering an organizer and a customer
4. ✅ Creating an event as organizer
5. ✅ Browsing events (public access)
6. ✅ Booking tickets as customer
7. ✅ **Background Task 1**: Show the booking confirmation email in console
8. ✅ Updating an event as organizer
9. ✅ **Background Task 2**: Show the event update notification in console
10. ✅ Viewing bookings (both customer and organizer views)
11. ✅ Demonstrating role-based access control (try accessing organizer endpoint as customer)

## Troubleshooting

- **Port already in use**: Change the port in `app.py` (last line)
- **Module not found**: Run `pip install -r requirements.txt`
- **Database errors**: Delete `event_booking.db` and restart the app
