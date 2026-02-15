"""
Demo Script for Event Booking System
This script demonstrates all features with sample data
"""

import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}\n")

def print_step(step_num, text):
    print(f"{Colors.BOLD}{Colors.CYAN}[Step {step_num}] {text}{Colors.END}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def demo():
    print_header("EVENT BOOKING SYSTEM - COMPLETE DEMO")
    
    # Step 1: Register Organizer
    print_step(1, "Registering Event Organizer")
    organizer = {
        "email": "john.organizer@eventco.com",
        "password": "secure123",
        "name": "John Smith",
        "role": "organizer"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=organizer)
    if response.status_code == 201:
        print_success("Organizer registered successfully")
        print_info(f"Name: {organizer['name']}, Email: {organizer['email']}")
    time.sleep(0.5)
    
    # Step 2: Register Multiple Customers
    print_step(2, "Registering Customers")
    customers = [
        {"email": "alice@example.com", "password": "pass123", "name": "Alice Johnson", "role": "customer"},
        {"email": "bob@example.com", "password": "pass123", "name": "Bob Williams", "role": "customer"},
        {"email": "carol@example.com", "password": "pass123", "name": "Carol Davis", "role": "customer"}
    ]
    
    for customer in customers:
        response = requests.post(f"{BASE_URL}/auth/register", json=customer)
        if response.status_code == 201:
            print_success(f"Customer registered: {customer['name']}")
    time.sleep(0.5)
    
    # Step 3: Login as Organizer
    print_step(3, "Logging in as Organizer")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": organizer['email'],
        "password": organizer['password']
    })
    organizer_token = response.json()['access_token']
    print_success("Organizer logged in successfully")
    print_info(f"JWT Token: {organizer_token[:30]}...")
    time.sleep(0.5)
    
    # Step 4: Create Multiple Events
    print_step(4, "Creating Events")
    events = [
        {
            "title": "Tech Summit 2024",
            "description": "Annual technology conference featuring AI, Cloud, and Web3",
            "date": (datetime.now() + timedelta(days=45)).isoformat(),
            "location": "Silicon Valley Convention Center",
            "total_tickets": 500,
            "price": 299.99
        },
        {
            "title": "Music Festival - Summer Vibes",
            "description": "3-day outdoor music festival with top artists",
            "date": (datetime.now() + timedelta(days=60)).isoformat(),
            "location": "Central Park, New York",
            "total_tickets": 2000,
            "price": 149.99
        },
        {
            "title": "Startup Pitch Night",
            "description": "Watch innovative startups pitch to investors",
            "date": (datetime.now() + timedelta(days=15)).isoformat(),
            "location": "Innovation Hub, San Francisco",
            "total_tickets": 150,
            "price": 49.99
        }
    ]
    
    headers = {"Authorization": f"Bearer {organizer_token}"}
    event_ids = []
    
    for event in events:
        response = requests.post(f"{BASE_URL}/events", json=event, headers=headers)
        if response.status_code == 201:
            event_id = response.json()['event']['id']
            event_ids.append(event_id)
            print_success(f"Event created: {event['title']} (ID: {event_id})")
    time.sleep(0.5)
    
    # Step 5: Browse Events (Public Access)
    print_step(5, "Browsing Events (Public Access - No Authentication)")
    response = requests.get(f"{BASE_URL}/events")
    events_list = response.json()['events']
    print_success(f"Found {len(events_list)} events")
    for event in events_list:
        print_info(f"  • {event['title']} - ${event['price']} - {event['available_tickets']} tickets available")
    time.sleep(0.5)
    
    # Step 6: Customers Book Tickets
    print_step(6, "Customers Booking Tickets")
    print_warning("Watch the server console for BOOKING CONFIRMATION EMAILS!")
    
    bookings = [
        {"customer": customers[0], "event_id": event_ids[0], "tickets": 2},
        {"customer": customers[1], "event_id": event_ids[0], "tickets": 3},
        {"customer": customers[2], "event_id": event_ids[1], "tickets": 5},
        {"customer": customers[0], "event_id": event_ids[2], "tickets": 1}
    ]
    
    for booking in bookings:
        # Login as customer
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": booking['customer']['email'],
            "password": booking['customer']['password']
        })
        customer_token = response.json()['access_token']
        
        # Book tickets
        headers = {"Authorization": f"Bearer {customer_token}"}
        response = requests.post(f"{BASE_URL}/bookings", json={
            "event_id": booking['event_id'],
            "tickets_count": booking['tickets']
        }, headers=headers)
        
        if response.status_code == 201:
            booking_data = response.json()['booking']
            print_success(f"{booking['customer']['name']} booked {booking['tickets']} tickets for {booking_data['event_title']}")
            print_info(f"  Total: ${booking_data['total_price']}")
        
        time.sleep(1)  # Wait to see background task
    
    # Step 7: View Organizer Dashboard
    print_step(7, "Viewing Organizer Dashboard")
    headers = {"Authorization": f"Bearer {organizer_token}"}
    response = requests.get(f"{BASE_URL}/organizer/events", headers=headers)
    organizer_events = response.json()['events']
    print_success(f"Organizer has {len(organizer_events)} events")
    
    for event in organizer_events:
        print_info(f"  • {event['title']}: {event['total_tickets'] - event['available_tickets']} tickets sold")
    time.sleep(0.5)
    
    # Step 8: View Event Bookings
    print_step(8, "Viewing Bookings for First Event")
    response = requests.get(f"{BASE_URL}/organizer/events/{event_ids[0]}/bookings", headers=headers)
    bookings_list = response.json()['bookings']
    print_success(f"Event has {len(bookings_list)} bookings")
    
    for booking in bookings_list:
        print_info(f"  • {booking['customer_name']}: {booking['tickets_count']} tickets - ${booking['total_price']}")
    time.sleep(0.5)
    
    # Step 9: Update Event
    print_step(9, "Updating Event Details")
    print_warning("Watch the server console for EVENT UPDATE NOTIFICATIONS!")
    
    update_data = {
        "title": "Tech Summit 2024 - EXTENDED PROGRAM",
        "description": "Annual technology conference featuring AI, Cloud, Web3, and Blockchain",
        "location": "Silicon Valley Convention Center - Main Hall"
    }
    
    response = requests.put(f"{BASE_URL}/events/{event_ids[0]}", json=update_data, headers=headers)
    if response.status_code == 200:
        print_success("Event updated successfully")
        updated_event = response.json()['event']
        print_info(f"  New title: {updated_event['title']}")
        print_info(f"  New location: {updated_event['location']}")
    
    time.sleep(2)  # Wait to see background task
    
    # Step 10: Test Role-Based Access Control
    print_step(10, "Testing Role-Based Access Control")
    
    # Try to create event as customer (should fail)
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": customers[0]['email'],
        "password": customers[0]['password']
    })
    customer_token = response.json()['access_token']
    
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = requests.post(f"{BASE_URL}/events", json=events[0], headers=headers)
    
    if response.status_code == 403:
        print_success("Access Control Working: Customer cannot create events")
        print_info(f"  Error: {response.json()['error']}")
    
    # Try to book tickets as organizer (should fail)
    headers = {"Authorization": f"Bearer {organizer_token}"}
    response = requests.post(f"{BASE_URL}/bookings", json={
        "event_id": event_ids[0],
        "tickets_count": 1
    }, headers=headers)
    
    if response.status_code == 403:
        print_success("Access Control Working: Organizer cannot book tickets")
        print_info(f"  Error: {response.json()['error']}")
    
    time.sleep(0.5)
    
    # Final Summary
    print_header("DEMO COMPLETED SUCCESSFULLY")
    print(f"{Colors.GREEN}✓ User Registration & Authentication{Colors.END}")
    print(f"{Colors.GREEN}✓ Event Creation & Management{Colors.END}")
    print(f"{Colors.GREEN}✓ Ticket Booking System{Colors.END}")
    print(f"{Colors.GREEN}✓ Background Task 1: Booking Confirmation Emails{Colors.END}")
    print(f"{Colors.GREEN}✓ Background Task 2: Event Update Notifications{Colors.END}")
    print(f"{Colors.GREEN}✓ Role-Based Access Control{Colors.END}")
    print(f"{Colors.GREEN}✓ Organizer Dashboard{Colors.END}")
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}Check the server console to see all background tasks!{Colors.END}\n")

if __name__ == "__main__":
    try:
        print(f"{Colors.BOLD}Starting demo in 2 seconds...{Colors.END}")
        time.sleep(2)
        demo()
    except requests.exceptions.ConnectionError:
        print(f"\n{Colors.RED}❌ Error: Could not connect to the API server.{Colors.END}")
        print(f"{Colors.YELLOW}Please make sure the server is running: python app.py{Colors.END}\n")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Demo interrupted by user{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {str(e)}{Colors.END}\n")
