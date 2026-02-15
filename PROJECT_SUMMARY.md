# Event Booking System - Project Summary

## 🎯 Project Overview

A complete backend API system for event booking that supports two types of users (Event Organizers and Customers) with role-based access control and asynchronous background tasks.

---

## ✨ Key Features Implemented

### 1. User Management
- ✅ User registration with role selection (Organizer/Customer)
- ✅ Secure authentication using JWT tokens
- ✅ Password hashing for security
- ✅ Role-based access control

### 2. Event Management (Organizer)
- ✅ Create events with full details
- ✅ Update events (triggers notifications)
- ✅ Delete events
- ✅ View all owned events
- ✅ View bookings for each event

### 3. Event Browsing (Public)
- ✅ List all available events
- ✅ View event details
- ✅ No authentication required

### 4. Ticket Booking (Customer)
- ✅ Book tickets for events
- ✅ Automatic ticket availability tracking
- ✅ View personal booking history
- ✅ Price calculation

### 5. Background Tasks
- ✅ **Task 1**: Booking confirmation email (async)
- ✅ **Task 2**: Event update notifications (async)
- ✅ Implemented using Python threading
- ✅ Console logging for demonstration

### 6. Security & Access Control
- ✅ JWT-based authentication
- ✅ Role-based authorization
- ✅ Ownership verification
- ✅ Input validation

---

## 📁 Project Structure

```
Event/
├── app.py                      # Main Flask application with all endpoints
├── models.py                   # Database models (User, Event, Booking)
├── auth.py                     # Authentication & authorization utilities
├── background_tasks.py         # Async task handlers
├── requirements.txt            # Python dependencies
├── README.md                   # Main documentation with design decisions
├── API_DOCUMENTATION.md        # Complete API reference
├── ARCHITECTURE.md             # System architecture diagrams
├── QUICKSTART.md              # Quick start guide
├── VIDEO_DEMO_SCRIPT.md       # Script for video recording
├── TROUBLESHOOTING.md         # Common issues and solutions
├── test_api.py                # Automated API testing script
├── demo.py                    # Interactive demo with sample data
├── postman_collection.json    # Postman API collection
└── .gitignore                 # Git ignore file
```

---

## 🛠️ Technology Stack

| Component | Technology | Reason |
|-----------|-----------|---------|
| **Framework** | Flask | Lightweight, easy to set up, perfect for RESTful APIs |
| **Database** | SQLite + SQLAlchemy | No external setup, easy to demo, ORM for clean code |
| **Authentication** | JWT (Flask-JWT-Extended) | Stateless, scalable, industry standard |
| **Background Tasks** | Python Threading | No external dependencies, simple for demo |
| **Password Security** | Werkzeug Security | Built-in, secure hashing (PBKDF2) |

---

## 🔌 API Endpoints Summary

### Authentication (No Auth)
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login and get token

### Events (Public)
- `GET /api/events` - List all events
- `GET /api/events/<id>` - Get event details

### Events (Organizer Only)
- `POST /api/events` - Create event
- `PUT /api/events/<id>` - Update event ⚡ Triggers notification
- `DELETE /api/events/<id>` - Delete event
- `GET /api/organizer/events` - Get my events
- `GET /api/organizer/events/<id>/bookings` - Get event bookings

### Bookings (Customer Only)
- `POST /api/bookings` - Book tickets ⚡ Triggers confirmation
- `GET /api/bookings` - Get my bookings

---

## 🎬 How to Run

### Quick Start (3 steps)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
python app.py

# 3. Run the demo (in another terminal)
python demo.py
```

### Manual Testing
```bash
# Option 1: Use the test script
python test_api.py

# Option 2: Import Postman collection
# Import postman_collection.json into Postman

# Option 3: Use curl commands
# See QUICKSTART.md for examples
```

---

## 🎥 Video Demo Checklist

When recording your video, make sure to show:

- [x] **Your face** (required throughout the video)
- [x] **Project structure** in IDE
- [x] **Starting the server**
- [x] **User registration** (both organizer and customer)
- [x] **Event creation** by organizer
- [x] **Public event browsing** (no auth)
- [x] **Ticket booking** by customer
- [x] **Background Task 1**: Booking confirmation in console
- [x] **Event update** by organizer
- [x] **Background Task 2**: Update notifications in console
- [x] **Role-based access control** (show 403 errors)
- [x] **Organizer dashboard** (events and bookings)

**Duration**: 3-4 minutes (max 5 minutes)
**Language**: English
**Script**: See VIDEO_DEMO_SCRIPT.md

---

## 📊 Database Schema

```
Users (id, email, password_hash, name, role)
  ↓ 1:N
Events (id, title, description, date, location, total_tickets, available_tickets, price, organizer_id)
  ↓ 1:N
Bookings (id, event_id, customer_id, tickets_count, total_price, booking_date)
```

---

## 🔐 Security Features

1. **Password Hashing**: PBKDF2 algorithm via Werkzeug
2. **JWT Tokens**: Stateless authentication with 24-hour expiry
3. **Role-Based Access**: Middleware enforces role requirements
4. **Ownership Verification**: Users can only modify their own resources
5. **Input Validation**: All endpoints validate required fields

---

## 🚀 Background Tasks

### Task 1: Booking Confirmation Email
- **Trigger**: When customer books tickets
- **Action**: Simulates sending confirmation email
- **Implementation**: Async thread with console output
- **Data**: Customer name, email, event details, booking info

### Task 2: Event Update Notification
- **Trigger**: When organizer updates event
- **Action**: Notifies all customers who booked tickets
- **Implementation**: Async thread with console output
- **Data**: Event details, list of affected customers

---

## 📝 Design Decisions (Documented in README.md)

### Why Flask?
- Lightweight and minimal setup
- Perfect for RESTful APIs
- Large ecosystem and community
- Easy to understand and demo

### Why SQLite?
- No external database setup required
- Perfect for development and demo
- Easy to reset and test
- Can be easily migrated to PostgreSQL/MySQL

### Why Threading for Background Tasks?
- No external dependencies (Redis, RabbitMQ)
- Simple to implement and understand
- Sufficient for demo purposes
- Can be easily replaced with Celery for production

### Why JWT?
- Stateless authentication
- Scalable (no server-side sessions)
- Industry standard
- Works well with mobile/web clients

---

## 🧪 Testing

### Automated Testing
```bash
# Full automated test
python test_api.py

# Interactive demo with sample data
python demo.py
```

### Manual Testing
```bash
# Import into Postman
postman_collection.json

# Or use curl commands
# See QUICKSTART.md for examples
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Main documentation with design decisions |
| `API_DOCUMENTATION.md` | Complete API reference with examples |
| `ARCHITECTURE.md` | System architecture and diagrams |
| `QUICKSTART.md` | Quick start guide for testing |
| `VIDEO_DEMO_SCRIPT.md` | Script for recording demo video |
| `TROUBLESHOOTING.md` | Common issues and solutions |

---

## 🎯 Requirements Fulfilled

✅ **Two User Types**: Organizers and Customers with different permissions
✅ **Role-Based Access Control**: Middleware enforces role requirements
✅ **Event Management**: Full CRUD operations for organizers
✅ **Ticket Booking**: Customers can browse and book tickets
✅ **Background Task 1**: Booking confirmation (console log)
✅ **Background Task 2**: Event update notification (console log)
✅ **Async Processing**: Threading for background tasks
✅ **Documentation**: All design decisions documented in README
✅ **Clean Code**: Well-organized, minimal, and maintainable

---

## 🔄 Future Enhancements

If this were a production system, consider:

1. **Real Email Service**: SendGrid, AWS SES, or Mailgun
2. **Production Task Queue**: Celery with Redis/RabbitMQ
3. **Database**: PostgreSQL or MySQL
4. **Payment Integration**: Stripe or PayPal
5. **Rate Limiting**: Prevent API abuse
6. **Caching**: Redis for frequently accessed data
7. **File Upload**: Event images and attachments
8. **Search & Filters**: Advanced event search
9. **Ticket Cancellation**: Refund system
10. **Admin Panel**: Web interface for management

---

## 🎓 Learning Outcomes

This project demonstrates:
- RESTful API design principles
- Authentication and authorization
- Database modeling and relationships
- Asynchronous task processing
- Role-based access control
- Clean code organization
- Comprehensive documentation

---

## 📞 Support

If you encounter any issues:
1. Check `TROUBLESHOOTING.md`
2. Review `API_DOCUMENTATION.md`
3. Check server console for error messages
4. Verify authentication tokens
5. Restart the server

---

## 🏁 Getting Started Now

```bash
# Clone/Navigate to project
cd f:\Users\Desktop\Event

# Install dependencies
pip install -r requirements.txt

# Start server
python app.py

# In another terminal, run demo
python demo.py

# Watch the magic happen! ✨
```

---

## 📹 Recording Your Video

1. Read `VIDEO_DEMO_SCRIPT.md` thoroughly
2. Practice the demo once before recording
3. Ensure your face is visible
4. Speak clearly in English
5. Show both background tasks in action
6. Demonstrate role-based access control
7. Keep it 3-4 minutes (max 5)

**Good luck with your demo! 🎬**
