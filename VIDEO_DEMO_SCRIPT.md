# Video Demo Script (3-4 minutes)

## Preparation Checklist
- [ ] Camera positioned to show your face
- [ ] Microphone working properly
- [ ] Screen recording software ready (Loom, OBS, etc.)
- [ ] Terminal/Console visible
- [ ] Postman or API testing tool ready
- [ ] Server NOT running yet (start during demo)

---

## Demo Script

### Introduction (30 seconds)
**[Show your face on camera]**

"Hello! My name is [Your Name], and I'm going to demonstrate the Event Booking System I've built. This is a complete backend API that supports two types of users: Event Organizers and Customers. The system includes role-based access control and two background tasks for notifications."

---

### Part 1: System Overview (30 seconds)
**[Show project structure in IDE]**

"Let me quickly show you the project structure. I've built this using Flask, SQLAlchemy for the database, and JWT for authentication. The main components are:
- app.py - the main API server
- models.py - database models for Users, Events, and Bookings
- auth.py - authentication and role-based access control
- background_tasks.py - async tasks for emails and notifications"

---

### Part 2: Starting the Server (15 seconds)
**[Open terminal and run the server]**

```bash
python app.py
```

"Let me start the server. As you can see, it's running on localhost port 5000."

---

### Part 3: Running the Demo (2 minutes)
**[Open another terminal and run demo script]**

```bash
python demo.py
```

"Now I'll run the automated demo script that tests all the features."

**[As the demo runs, explain what's happening]**

"Watch as the system:
1. Registers an organizer and multiple customers
2. The organizer logs in and creates several events
3. Anyone can browse events without authentication - this is public access
4. Customers log in and book tickets

**[Point to server console]**
5. HERE - you can see the first background task: Booking Confirmation Email being sent
6. The organizer can view all their events and bookings
7. Now the organizer updates an event...

**[Point to server console again]**
8. And HERE - the second background task: Event Update Notifications are sent to all customers who booked tickets

9. Finally, we test role-based access control - customers can't create events, and organizers can't book tickets"

---

### Part 4: Manual API Testing (45 seconds)
**[Switch to Postman or show curl commands]**

"Let me also show you a quick manual test. I'll use Postman to:
1. Login as a customer
2. Browse available events
3. Book tickets for an event

**[Execute the requests]**

And again, you can see the booking confirmation in the server console."

---

### Part 5: Key Features Summary (30 seconds)
**[Show your face again]**

"To summarize, this Event Booking System includes:

✓ Complete user authentication with JWT tokens
✓ Role-based access control - Organizers manage events, Customers book tickets
✓ Full CRUD operations for events
✓ Ticket booking with availability tracking
✓ Background Task 1: Booking confirmation emails
✓ Background Task 2: Event update notifications to all affected customers
✓ RESTful API design with proper error handling

All design decisions are documented in the README file, including why I chose Flask, SQLite, and threading for background tasks."

---

### Closing (15 seconds)
**[Show your face]**

"Thank you for watching! The complete code, documentation, and API collection are available in the repository. Feel free to test all the endpoints using the provided Postman collection or test scripts."

---

## Tips for Recording

1. **Speak Clearly**: Speak in English at a moderate pace
2. **Show Your Face**: Keep your face visible throughout, especially during intro and outro
3. **Highlight Important Parts**: Point to or highlight the console when background tasks run
4. **Don't Rush**: Take your time to explain what's happening
5. **Show Enthusiasm**: Be confident and enthusiastic about your work
6. **Test First**: Do a practice run before recording
7. **Keep It Concise**: Aim for 3-4 minutes, maximum 5 minutes

---

## Alternative: Manual Demo Flow

If you prefer to demo manually instead of using the script:

### Step-by-Step Manual Demo

1. **Register Organizer** (POST /auth/register)
   ```json
   {
     "email": "organizer@test.com",
     "password": "pass123",
     "name": "John Organizer",
     "role": "organizer"
   }
   ```

2. **Register Customer** (POST /auth/register)
   ```json
   {
     "email": "customer@test.com",
     "password": "pass123",
     "name": "Jane Customer",
     "role": "customer"
   }
   ```

3. **Login as Organizer** (POST /auth/login)
   - Copy the JWT token

4. **Create Event** (POST /events with organizer token)
   ```json
   {
     "title": "Tech Conference 2024",
     "description": "Annual tech conference",
     "date": "2024-12-31T10:00:00",
     "location": "Convention Center",
     "total_tickets": 100,
     "price": 99.99
   }
   ```

5. **Browse Events** (GET /events - no auth)
   - Show that anyone can view events

6. **Login as Customer** (POST /auth/login)
   - Copy the JWT token

7. **Book Tickets** (POST /bookings with customer token)
   ```json
   {
     "event_id": 1,
     "tickets_count": 3
   }
   ```
   - **POINT TO CONSOLE** - Show booking confirmation email

8. **Update Event** (PUT /events/1 with organizer token)
   ```json
   {
     "title": "Tech Conference 2024 - UPDATED",
     "location": "Grand Convention Center"
   }
   ```
   - **POINT TO CONSOLE** - Show event update notification

9. **Test Access Control**
   - Try to create event with customer token (should fail)
   - Show the 403 error

10. **Show Organizer Dashboard** (GET /organizer/events)
    - Show all events and bookings

---

## Common Issues During Demo

### Issue: Server not starting
**Solution**: Check if port 5000 is already in use. Change port in app.py if needed.

### Issue: Database errors
**Solution**: Delete event_booking.db file and restart server.

### Issue: Background tasks not showing
**Solution**: Make sure you're looking at the correct terminal where app.py is running.

### Issue: Token expired
**Solution**: Login again to get a new token.

---

## What to Emphasize

1. **Background Tasks**: This is a key requirement - make sure to clearly show both tasks running
2. **Role-Based Access**: Demonstrate that access control works properly
3. **Clean Code**: Mention that the code is well-organized and documented
4. **Design Decisions**: Reference the README where all decisions are documented
5. **Scalability**: Mention that the threading approach can be easily replaced with Celery/Redis for production

---

## Recording Checklist

Before you finish recording, make sure you've shown:
- [x] Your face clearly visible
- [x] Server starting successfully
- [x] User registration (both roles)
- [x] Event creation
- [x] Ticket booking
- [x] Background Task 1: Booking confirmation
- [x] Background Task 2: Event update notification
- [x] Role-based access control working
- [x] API responses showing proper data
- [x] Console logs for background tasks

Good luck with your recording! 🎥
