import threading
from datetime import datetime

def send_booking_confirmation_email(booking_data):
    """
    Background Task 1: Booking Confirmation Email
    Simulates sending a booking confirmation email to the customer
    """
    def task():
        print("\n" + "="*60)
        print("📧 BACKGROUND TASK: Booking Confirmation Email")
        print("="*60)
        print(f"To: {booking_data['customer_email']}")
        print(f"Subject: Booking Confirmation - {booking_data['event_title']}")
        print(f"\nDear {booking_data['customer_name']},")
        print(f"\nYour booking has been confirmed!")
        print(f"\nEvent: {booking_data['event_title']}")
        print(f"Tickets: {booking_data['tickets_count']}")
        print(f"Total Price: ${booking_data['total_price']}")
        print(f"Booking Date: {booking_data['booking_date']}")
        print(f"\nThank you for your booking!")
        print("="*60 + "\n")
    
    thread = threading.Thread(target=task)
    thread.daemon = True
    thread.start()

def send_event_update_notification(event_data, customers):
    """
    Background Task 2: Event Update Notification
    Notifies all customers who have booked tickets for the updated event
    """
    def task():
        print("\n" + "="*60)
        print("🔔 BACKGROUND TASK: Event Update Notification")
        print("="*60)
        print(f"Event Updated: {event_data['title']}")
        print(f"Updated At: {datetime.utcnow().isoformat()}")
        print(f"\nNotifying {len(customers)} customer(s):")
        print("-"*60)
        
        for customer in customers:
            print(f"\n📨 Sending notification to:")
            print(f"   Name: {customer['name']}")
            print(f"   Email: {customer['email']}")
            print(f"   Message: The event '{event_data['title']}' has been updated.")
            print(f"   Please check the latest details.")
        
        print("\n" + "="*60 + "\n")
    
    thread = threading.Thread(target=task)
    thread.daemon = True
    thread.start()
