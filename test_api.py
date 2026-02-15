import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"📍 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print(f"{'='*60}\n")

def test_api():
    print("\n🎯 Starting Event Booking System API Test\n")
    
    # 1. Register Organizer
    print("1️⃣ Registering Event Organizer...")
    organizer_data = {
        "email": "organizer@example.com",
        "password": "password123",
        "name": "John Organizer",
        "role": "organizer"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=organizer_data)
    print_response("Register Organizer", response)
    
    # 2. Register Customer
    print("2️⃣ Registering Customer...")
    customer_data = {
        "email": "customer@example.com",
        "password": "password123",
        "name": "Jane Customer",
        "role": "customer"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=customer_data)
    print_response("Register Customer", response)
    
    # 3. Login as Organizer
    print("3️⃣ Logging in as Organizer...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "organizer@example.com",
        "password": "password123"
    })
    print_response("Login Organizer", response)
    organizer_token = response.json()['access_token']
    
    # 4. Create Event
    print("4️⃣ Creating Event...")
    event_date = (datetime.now() + timedelta(days=30)).isoformat()
    event_data = {
        "title": "Tech Conference 2024",
        "description": "Annual technology conference with industry leaders",
        "date": event_date,
        "location": "Convention Center, New York",
        "total_tickets": 100,
        "price": 99.99
    }
    headers = {"Authorization": f"Bearer {organizer_token}"}
    response = requests.post(f"{BASE_URL}/events", json=event_data, headers=headers)
    print_response("Create Event", response)
    event_id = response.json()['event']['id']
    
    # 5. Get All Events (Public)
    print("5️⃣ Getting All Events (Public Access)...")
    response = requests.get(f"{BASE_URL}/events")
    print_response("Get All Events", response)
    
    # 6. Login as Customer
    print("6️⃣ Logging in as Customer...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "customer@example.com",
        "password": "password123"
    })
    print_response("Login Customer", response)
    customer_token = response.json()['access_token']
    
    # 7. Book Tickets
    print("7️⃣ Booking Tickets (Watch for Background Task)...")
    booking_data = {
        "event_id": event_id,
        "tickets_count": 3
    }
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = requests.post(f"{BASE_URL}/bookings", json=booking_data, headers=headers)
    print_response("Book Tickets", response)
    
    import time
    time.sleep(1)  # Wait for background task to complete
    
    # 8. Get Customer Bookings
    print("8️⃣ Getting Customer Bookings...")
    response = requests.get(f"{BASE_URL}/bookings", headers=headers)
    print_response("Get Customer Bookings", response)
    
    # 9. Update Event (Triggers Notification)
    print("9️⃣ Updating Event (Watch for Background Task)...")
    update_data = {
        "title": "Tech Conference 2024 - UPDATED",
        "location": "Grand Convention Center, New York"
    }
    headers = {"Authorization": f"Bearer {organizer_token}"}
    response = requests.put(f"{BASE_URL}/events/{event_id}", json=update_data, headers=headers)
    print_response("Update Event", response)
    
    time.sleep(1)  # Wait for background task to complete
    
    # 10. Get Organizer's Events
    print("🔟 Getting Organizer's Events...")
    response = requests.get(f"{BASE_URL}/organizer/events", headers=headers)
    print_response("Get Organizer Events", response)
    
    # 11. Get Event Bookings (Organizer)
    print("1️⃣1️⃣ Getting Event Bookings (Organizer View)...")
    response = requests.get(f"{BASE_URL}/organizer/events/{event_id}/bookings", headers=headers)
    print_response("Get Event Bookings", response)
    
    print("\n✅ API Test Completed Successfully!\n")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API server.")
        print("Please make sure the server is running: python app.py\n")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
