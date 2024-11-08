import smtplib
import os


# Function to send an email
def send_email():
    # Store your email and password in environment variables for security
    email = os.environ.get("SENDER_EMAIL")  # Set this in your environment
    password = os.environ.get("EMAIL_PASSWORD")  # Set this in your environment

    if not email or not password:
        print("Please set your email and password in environment variables.")
        return

    # Get recipient details and message
    receiver_email = input("Enter receiver's email: ")
    subject = input("SUBJECT: ")
    message = input("MESSAGE: ")
    text = f"Subject: {subject}\n\n{message}"

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Enable security

        # Login and send email
        server.login(email, password)
        server.sendmail(email, receiver_email, text)
        print(f"Email has been sent to {receiver_email}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server.quit()


if __name__ == '__main__':
    send_email()
