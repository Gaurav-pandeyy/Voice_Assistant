import smtplib
import os



def send_email(subject, message):
    email = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("EMAIL_PASSWORD")

    if not email or not password:
        print("Please set your email and password in environment variables.")
        return "Email sending failed: Missing credentials"

    receiver_email = "gaurapande871@gmail.com"
    subject = (f"SUBJECT: {subject}")
    message = (f"MESSAGE: {message}")
    text = f"Subject: {subject}\n\n{message}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Enable security

        server.login(email, password)
        server.sendmail(email, receiver_email, text)
        print(f"The Email to {receiver_email}")
        return "Has been  sent successfully!"
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Email sending failed: {e}"
    finally:
        server.quit()
