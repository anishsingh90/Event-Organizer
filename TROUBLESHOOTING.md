# Troubleshooting Guide

## Installation Issues

### Issue: pip install fails
**Error**: `Could not find a version that satisfies the requirement...`

**Solution**:
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

---

### Issue: Python version incompatibility
**Error**: `SyntaxError` or version-related errors

**Solution**:
Ensure you're using Python 3.8 or higher:
```bash
python --version
```

If you have multiple Python versions:
```bash
python3 --version
python3 -m pip install -r requirements.txt
python3 app.py
```

---

## Server Issues

### Issue: Port 5000 already in use
**Error**: `Address already in use` or `OSError: [Errno 48]`

**Solution 1**: Kill the process using port 5000
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

**Solution 2**: Change the port in app.py
```python
# Last line of app.py
app.run(debug=True, port=5001)  # Change to any available port
```

---

### Issue: Server starts but crashes immediately
**Error**: Various database or import errors

**Solution**:
1. Delete the database file:
```bash
# Windows
del event_booking.db

# Mac/Linux
rm event_booking.db
```

2. Restart the server:
```bash
python app.py
```

---

## Database Issues

### Issue: Database locked
**Error**: `sqlite3.OperationalError: database is locked`

**Solution**:
1. Close all connections to the database
2. Delete the database file
3. Restart the server

```bash
# Windows
del event_booking.db

# Mac/Linux
rm event_booking.db

python app.py
```

---

### Issue: Table doesn't exist
**Error**: `sqlite3.OperationalError: no such table: users`

**Solution**:
The database wasn't initialized properly. Delete and restart:
```bash
# Windows
del event_booking.db

# Mac/Linux
rm event_booking.db

python app.py
```

---

## API Testing Issues

### Issue: 401 Unauthorized error
**Error**: `{"error": "Missing Authorization Header"}`

**Solution**:
Make sure you're including the JWT token in the Authorization header:
```
Authorization: Bearer <your_token_here>
```

In Postman:
1. Go to the "Authorization" tab
2. Select "Bearer Token"
3. Paste your token

In curl:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:5000/api/events
```

---

### Issue: 403 Forbidden error
**Error**: `{"error": "Access denied. Organizer role required"}`

**Solution**:
You're trying to access an endpoint that requires a different role:
- Organizer endpoints: Create/Update/Delete events
- Customer endpoints: Book tickets

Make sure you're logged in with the correct role and using the right token.

---

### Issue: Token expired
**Error**: `{"msg": "Token has expired"}`

**Solution**:
Login again to get a new token:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","password":"yourpassword"}'
```

---

### Issue: 400 Bad Request - Invalid date format
**Error**: `{"error": "Invalid date format. Use ISO format"}`

**Solution**:
Use ISO 8601 date format:
```json
{
  "date": "2024-12-31T10:00:00"
}
```

Not:
```json
{
  "date": "12/31/2024"  // ❌ Wrong format
}
```

---

### Issue: 400 Not enough tickets
**Error**: `{"error": "Not enough tickets available"}`

**Solution**:
The event doesn't have enough available tickets. Check available tickets:
```bash
curl http://localhost:5000/api/events/1
```

---

## Background Task Issues

### Issue: Background tasks not showing in console
**Problem**: Booking confirmation or event update notifications not appearing

**Solution**:
1. Make sure you're looking at the correct terminal where `app.py` is running
2. The background tasks print to the server console, not the client
3. Wait 1-2 seconds after the API call for the task to complete

---

### Issue: Background tasks showing but with errors
**Error**: Various Python errors in background task

**Solution**:
Check the server console for the full error message. Common issues:
- Database connection closed: Restart the server
- Missing data: Check that the booking/event was created successfully

---

## Test Script Issues

### Issue: test_api.py fails with connection error
**Error**: `requests.exceptions.ConnectionError`

**Solution**:
Make sure the server is running in another terminal:
```bash
# Terminal 1
python app.py

# Terminal 2
python test_api.py
```

---

### Issue: demo.py shows no colors
**Problem**: ANSI color codes not working on Windows

**Solution**:
This is normal on some Windows terminals. The demo will still work, just without colors.

To enable colors on Windows:
```bash
# Install colorama
pip install colorama

# Or use Windows Terminal instead of CMD
```

---

## Postman Issues

### Issue: Can't import postman_collection.json
**Error**: Import fails or shows errors

**Solution**:
1. Open Postman
2. Click "Import" button
3. Drag and drop `postman_collection.json`
4. If it fails, copy the JSON content and paste it directly

---

### Issue: Variables not working in Postman
**Problem**: `{{organizer_token}}` not being replaced

**Solution**:
Postman variables need to be set manually:
1. After login, copy the `access_token` from the response
2. Go to the "Variables" tab in Postman
3. Create a variable named `organizer_token`
4. Paste the token as the value

Or just paste the token directly in the Authorization header.

---

## Common Mistakes

### Mistake 1: Using wrong token for wrong role
**Problem**: Using customer token for organizer endpoints

**Solution**:
- Organizer endpoints: Use token from organizer login
- Customer endpoints: Use token from customer login

---

### Mistake 2: Forgetting Content-Type header
**Problem**: Server returns 400 or doesn't parse JSON

**Solution**:
Always include:
```
Content-Type: application/json
```

---

### Mistake 3: Not registering users first
**Problem**: Login fails because user doesn't exist

**Solution**:
Always register before login:
1. POST /api/auth/register
2. POST /api/auth/login

---

### Mistake 4: Trying to update someone else's event
**Problem**: 403 error when updating event

**Solution**:
You can only update events you created. Make sure:
1. You're logged in as the organizer who created the event
2. You're using the correct organizer token

---

## Performance Issues

### Issue: Server is slow
**Problem**: Requests taking too long

**Solution**:
1. This is a development server - it's not optimized for production
2. For better performance, use a production WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 app:app
```

---

### Issue: Database growing too large
**Problem**: event_booking.db file is very large

**Solution**:
For testing, you can reset the database:
```bash
# Windows
del event_booking.db

# Mac/Linux
rm event_booking.db

python app.py
```

---

## Getting Help

If you encounter an issue not listed here:

1. **Check the server console**: Most errors are logged there
2. **Check the API response**: Error messages usually explain the problem
3. **Verify your request**: Make sure all required fields are included
4. **Check authentication**: Ensure you're using a valid token
5. **Restart the server**: Many issues are resolved by restarting

---

## Debug Mode

To see more detailed error messages, the server is already running in debug mode.

If you need even more details, you can add print statements:

```python
# In app.py, add at the top of any endpoint:
print(f"Request data: {request.get_json()}")
print(f"Headers: {request.headers}")
```

---

## Still Having Issues?

1. Delete everything and start fresh:
```bash
# Windows
del event_booking.db
pip install -r requirements.txt
python app.py

# Mac/Linux
rm event_booking.db
pip install -r requirements.txt
python app.py
```

2. Check Python version:
```bash
python --version  # Should be 3.8 or higher
```

3. Check all dependencies are installed:
```bash
pip list
```

4. Make sure you're in the correct directory:
```bash
# Windows
cd f:\Users\Desktop\Event

# Mac/Linux
cd /path/to/Event
```
