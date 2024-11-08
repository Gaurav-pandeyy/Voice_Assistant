import smtplib
import os



def send_email():

    email = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("EMAIL_PASSWORD")

    if not email or not password:
        print("Please set your email and password in environment variables.")
        return


    receiver_email = input("Enter receiver's email: ")
    subject = input("SUBJECT: ")
    message = input("MESSAGE: ")
    text = f"Subject: {subject}\n\n{message}"

    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Enable security


        server.login(email, password)
        server.sendmail(email, receiver_email, text)
        print(f"Email has been sent to {receiver_email}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server.quit()


if __name__ == '__main__':
    send_email()
