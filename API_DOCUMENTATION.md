# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

---

## Endpoints

### 1. Authentication

#### Register User
**POST** `/auth/register`

Register a new user (organizer or customer).

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "role": "organizer"  // or "customer"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "organizer"
  }
}
```

**Errors:**
- `400`: Missing required fields or invalid role
- `400`: Email already registered

---

#### Login
**POST** `/auth/login`

Login and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "organizer"
  }
}
```

**Errors:**
- `400`: Missing email or password
- `401`: Invalid credentials

---

### 2. Events (Public Access)

#### Get All Events
**GET** `/events`

Get list of all events. No authentication required.

**Response (200):**
```json
{
  "events": [
    {
      "id": 1,
      "title": "Tech Conference 2024",
      "description": "Annual tech conference",
      "date": "2024-12-31T10:00:00",
      "location": "Convention Center",
      "total_tickets": 100,
      "available_tickets": 85,
      "price": 99.99,
      "organizer_id": 1,
      "organizer_name": "John Doe"
    }
  ]
}
```

---

#### Get Event by ID
**GET** `/events/<event_id>`

Get details of a specific event. No authentication required.

**Response (200):**
```json
{
  "event": {
    "id": 1,
    "title": "Tech Conference 2024",
    "description": "Annual tech conference",
    "date": "2024-12-31T10:00:00",
    "location": "Convention Center",
    "total_tickets": 100,
    "available_tickets": 85,
    "price": 99.99,
    "organizer_id": 1,
    "organizer_name": "John Doe"
  }
}
```

**Errors:**
- `404`: Event not found

---

### 3. Events (Organizer Only)

#### Create Event
**POST** `/events`

Create a new event. Requires organizer role.

**Headers:**
```
Authorization: Bearer <organizer_token>
```

**Request Body:**
```json
{
  "title": "Tech Conference 2024",
  "description": "Annual technology conference",
  "date": "2024-12-31T10:00:00",
  "location": "Convention Center",
  "total_tickets": 100,
  "price": 99.99
}
```

**Response (201):**
```json
{
  "message": "Event created successfully",
  "event": {
    "id": 1,
    "title": "Tech Conference 2024",
    "description": "Annual technology conference",
    "date": "2024-12-31T10:00:00",
    "location": "Convention Center",
    "total_tickets": 100,
    "available_tickets": 100,
    "price": 99.99,
    "organizer_id": 1,
    "organizer_name": "John Doe"
  }
}
```

**Errors:**
- `400`: Missing required fields
- `400`: Invalid date format
- `401`: Unauthorized (no token)
- `403`: Access denied (not an organizer)

---

#### Update Event
**PUT** `/events/<event_id>`

Update an existing event. Requires organizer role and ownership.

**Triggers:** Event Update Notification (Background Task 2)

**Headers:**
```
Authorization: Bearer <organizer_token>
```

**Request Body (all fields optional):**
```json
{
  "title": "Tech Conference 2024 - UPDATED",
  "description": "Updated description",
  "date": "2024-12-31T14:00:00",
  "location": "New Location",
  "price": 149.99
}
```

**Response (200):**
```json
{
  "message": "Event updated successfully",
  "event": {
    "id": 1,
    "title": "Tech Conference 2024 - UPDATED",
    "description": "Updated description",
    "date": "2024-12-31T14:00:00",
    "location": "New Location",
    "total_tickets": 100,
    "available_tickets": 85,
    "price": 149.99,
    "organizer_id": 1,
    "organizer_name": "John Doe"
  }
}
```

**Background Task:**
Notifies all customers who have booked tickets for this event.

**Errors:**
- `400`: Invalid date format
- `401`: Unauthorized
- `403`: You can only update your own events
- `404`: Event not found

---

#### Delete Event
**DELETE** `/events/<event_id>`

Delete an event. Requires organizer role and ownership.

**Headers:**
```
Authorization: Bearer <organizer_token>
```

**Response (200):**
```json
{
  "message": "Event deleted successfully"
}
```

**Errors:**
- `401`: Unauthorized
- `403`: You can only delete your own events
- `404`: Event not found

---

#### Get My Events
**GET** `/organizer/events`

Get all events created by the logged-in organizer.

**Headers:**
```
Authorization: Bearer <organizer_token>
```

**Response (200):**
```json
{
  "events": [
    {
      "id": 1,
      "title": "Tech Conference 2024",
      "description": "Annual tech conference",
      "date": "2024-12-31T10:00:00",
      "location": "Convention Center",
      "total_tickets": 100,
      "available_tickets": 85,
      "price": 99.99,
      "organizer_id": 1,
      "organizer_name": "John Doe"
    }
  ]
}
```

**Errors:**
- `401`: Unauthorized
- `403`: Organizer role required

---

#### Get Event Bookings
**GET** `/organizer/events/<event_id>/bookings`

Get all bookings for a specific event. Requires organizer role and ownership.

**Headers:**
```
Authorization: Bearer <organizer_token>
```

**Response (200):**
```json
{
  "bookings": [
    {
      "id": 1,
      "event_id": 1,
      "event_title": "Tech Conference 2024",
      "customer_id": 2,
      "customer_name": "Jane Customer",
      "customer_email": "customer@example.com",
      "tickets_count": 3,
      "total_price": 299.97,
      "booking_date": "2024-01-15T10:30:00"
    }
  ]
}
```

**Errors:**
- `401`: Unauthorized
- `403`: You can only view bookings for your own events
- `404`: Event not found

---

### 4. Bookings (Customer Only)

#### Book Tickets
**POST** `/bookings`

Book tickets for an event. Requires customer role.

**Triggers:** Booking Confirmation Email (Background Task 1)

**Headers:**
```
Authorization: Bearer <customer_token>
```

**Request Body:**
```json
{
  "event_id": 1,
  "tickets_count": 3
}
```

**Response (201):**
```json
{
  "message": "Booking successful",
  "booking": {
    "id": 1,
    "event_id": 1,
    "event_title": "Tech Conference 2024",
    "customer_id": 2,
    "customer_name": "Jane Customer",
    "customer_email": "customer@example.com",
    "tickets_count": 3,
    "total_price": 299.97,
    "booking_date": "2024-01-15T10:30:00"
  }
}
```

**Background Task:**
Sends booking confirmation email to the customer (simulated with console log).

**Errors:**
- `400`: Missing required fields
- `400`: Not enough tickets available
- `401`: Unauthorized
- `403`: Customer role required
- `404`: Event not found

---

#### Get My Bookings
**GET** `/bookings`

Get all bookings made by the logged-in customer.

**Headers:**
```
Authorization: Bearer <customer_token>
```

**Response (200):**
```json
{
  "bookings": [
    {
      "id": 1,
      "event_id": 1,
      "event_title": "Tech Conference 2024",
      "customer_id": 2,
      "customer_name": "Jane Customer",
      "customer_email": "customer@example.com",
      "tickets_count": 3,
      "total_price": 299.97,
      "booking_date": "2024-01-15T10:30:00"
    }
  ]
}
```

**Errors:**
- `401`: Unauthorized
- `403`: Customer role required

---

### 5. Health Check

#### Health Check
**GET** `/health`

Check if the API is running.

**Response (200):**
```json
{
  "status": "healthy",
  "message": "Event Booking API is running"
}
```

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request (invalid input)
- `401`: Unauthorized (missing or invalid token)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `500`: Internal Server Error

---

## Background Tasks

### Task 1: Booking Confirmation Email
**Triggered by:** POST `/bookings`

**Console Output:**
```
============================================================
📧 BACKGROUND TASK: Booking Confirmation Email
============================================================
To: customer@example.com
Subject: Booking Confirmation - Tech Conference 2024

Dear Jane Customer,

Your booking has been confirmed!

Event: Tech Conference 2024
Tickets: 3
Total Price: $299.97
Booking Date: 2024-01-15T10:30:00

Thank you for your booking!
============================================================
```

---

### Task 2: Event Update Notification
**Triggered by:** PUT `/events/<event_id>`

**Console Output:**
```
============================================================
🔔 BACKGROUND TASK: Event Update Notification
============================================================
Event Updated: Tech Conference 2024
Updated At: 2024-01-15T11:00:00
Notifying 2 customer(s):
------------------------------------------------------------

📨 Sending notification to:
   Name: Jane Customer
   Email: customer@example.com
   Message: The event 'Tech Conference 2024' has been updated.
   Please check the latest details.

📨 Sending notification to:
   Name: John Customer
   Email: john@example.com
   Message: The event 'Tech Conference 2024' has been updated.
   Please check the latest details.

============================================================
```

---

## Date Format

All dates should be in ISO 8601 format:
```
2024-12-31T10:00:00
```

You can also include timezone:
```
2024-12-31T10:00:00Z
2024-12-31T10:00:00+00:00
```
