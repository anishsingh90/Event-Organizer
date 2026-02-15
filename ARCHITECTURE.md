# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  (Postman / curl / Frontend App / test_api.py)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER (Flask)                           │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │     Auth     │  │    Events    │  │   Bookings   │          │
│  │  Endpoints   │  │  Endpoints   │  │  Endpoints   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────────────────────────────────────────┐           │
│  │         JWT Authentication Middleware             │           │
│  │         Role-Based Access Control (RBAC)          │           │
│  └──────────────────────────────────────────────────┘           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Database Layer  │  │  Background Tasks │  │   Auth Service   │
│   (SQLAlchemy)   │  │    (Threading)    │  │   (JWT/Hash)     │
│                  │  │                   │  │                  │
│  ┌────────────┐  │  │  ┌────────────┐  │  │  ┌────────────┐  │
│  │   Users    │  │  │  │   Email    │  │  │  │  Generate  │  │
│  │   Events   │  │  │  │Confirmation│  │  │  │   Tokens   │  │
│  │  Bookings  │  │  │  │            │  │  │  │            │  │
│  └────────────┘  │  │  └────────────┘  │  │  └────────────┘  │
│                  │  │                   │  │                  │
│                  │  │  ┌────────────┐  │  │  ┌────────────┐  │
│                  │  │  │   Event    │  │  │  │  Verify    │  │
│                  │  │  │ Notification│  │  │  │  Tokens    │  │
│                  │  │  └────────────┘  │  │  └────────────┘  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
         │
         ▼
┌──────────────────┐
│  SQLite Database │
│ event_booking.db │
└──────────────────┘
```

## Request Flow

### 1. User Registration/Login Flow
```
Client → POST /api/auth/register → Validate Data → Hash Password 
  → Save to DB → Return User Info

Client → POST /api/auth/login → Validate Credentials → Generate JWT 
  → Return Token + User Info
```

### 2. Create Event Flow (Organizer)
```
Client → POST /api/events + JWT Token → Verify Token → Check Role (Organizer)
  → Validate Event Data → Save to DB → Return Event Info
```

### 3. Book Tickets Flow (Customer)
```
Client → POST /api/bookings + JWT Token → Verify Token → Check Role (Customer)
  → Check Ticket Availability → Create Booking → Update Available Tickets
  → Trigger Background Task (Email Confirmation) → Return Booking Info
  
Background Thread → Print Confirmation Email to Console
```

### 4. Update Event Flow (Organizer)
```
Client → PUT /api/events/<id> + JWT Token → Verify Token → Check Role (Organizer)
  → Verify Ownership → Update Event → Get All Bookings for Event
  → Trigger Background Task (Notify Customers) → Return Updated Event
  
Background Thread → Print Notifications to Console for Each Customer
```

## Database Schema

```
┌─────────────────────┐
│       Users         │
├─────────────────────┤
│ id (PK)             │
│ email (UNIQUE)      │
│ password_hash       │
│ name                │
│ role                │◄──────┐
└─────────────────────┘       │
         │                    │
         │ 1:N                │ 1:N
         │                    │
         ▼                    │
┌─────────────────────┐       │
│       Events        │       │
├─────────────────────┤       │
│ id (PK)             │       │
│ title               │       │
│ description         │       │
│ date                │       │
│ location            │       │
│ total_tickets       │       │
│ available_tickets   │       │
│ price               │       │
│ organizer_id (FK)   │───────┘
│ created_at          │
└─────────────────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────────┐
│      Bookings       │
├─────────────────────┤
│ id (PK)             │
│ event_id (FK)       │───────┐
│ customer_id (FK)    │───────┼───┐
│ tickets_count       │       │   │
│ total_price         │       │   │
│ booking_date        │       │   │
└─────────────────────┘       │   │
                              │   │
                              ▼   ▼
                         References Events & Users
```

## Role-Based Access Control

```
┌──────────────────────────────────────────────────────────┐
│                    User Roles                             │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────┐      ┌─────────────────────┐   │
│  │     ORGANIZER       │      │      CUSTOMER       │   │
│  ├─────────────────────┤      ├─────────────────────┤   │
│  │ ✓ Create Events     │      │ ✓ Browse Events     │   │
│  │ ✓ Update Events     │      │ ✓ Book Tickets      │   │
│  │ ✓ Delete Events     │      │ ✓ View Bookings     │   │
│  │ ✓ View Bookings     │      │ ✗ Create Events     │   │
│  │ ✗ Book Tickets      │      │ ✗ Update Events     │   │
│  └─────────────────────┘      └─────────────────────┘   │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │              PUBLIC (No Auth)                    │    │
│  ├─────────────────────────────────────────────────┤    │
│  │ ✓ View Events List                              │    │
│  │ ✓ View Event Details                            │    │
│  │ ✗ All Other Operations                          │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

## Background Tasks Architecture

```
┌────────────────────────────────────────────────────────┐
│              Main Application Thread                    │
│                                                         │
│  API Request → Process → Trigger Background Task       │
│                              │                          │
│                              ▼                          │
│                    ┌──────────────────┐                │
│                    │  Create Thread   │                │
│                    │  (Daemon Mode)   │                │
│                    └──────────────────┘                │
│                              │                          │
└──────────────────────────────┼─────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────┐
│           Background Thread (Async)                     │
│                                                         │
│  Task 1: Booking Confirmation                          │
│  ┌──────────────────────────────────────────┐          │
│  │ • Receive booking data                   │          │
│  │ • Format email message                   │          │
│  │ • Print to console (simulated email)     │          │
│  └──────────────────────────────────────────┘          │
│                                                         │
│  Task 2: Event Update Notification                     │
│  ┌──────────────────────────────────────────┐          │
│  │ • Receive event data + customer list     │          │
│  │ • Loop through customers                 │          │
│  │ • Print notifications (simulated)        │          │
│  └──────────────────────────────────────────┘          │
└────────────────────────────────────────────────────────┘
```

## Security Features

1. **Password Hashing**: Using werkzeug.security (PBKDF2)
2. **JWT Authentication**: Stateless token-based auth
3. **Role-Based Access**: Middleware checks user role
4. **Input Validation**: Required fields validation
5. **Ownership Verification**: Users can only modify their own resources
