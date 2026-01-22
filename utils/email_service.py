import smtplib
from email.mime.text import MIMEText
import random
import string
import streamlit as st

# --- CONFIGURATION (Replace with your details or use st.secrets) ---
# You can set these in .streamlit/secrets.toml for security
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com" # <--- REPLACE THIS
SENDER_PASSWORD = "your_app_password" # <--- REPLACE THIS (App Password, not login password)

def generate_otp(length=6):
    """Generates a 6-digit numeric OTP."""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(receiver_email, otp_code):
    """Sends OTP via email. Returns (Success: bool, Message: str)."""
    subject = "Your Login OTP Code"
    body = f"Hello,\n\nYour One-Time Password (OTP) for login is:\n\n{otp_code}\n\nThis code expires in 5 minutes.\n\nBest regards,\nOTEP System"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email

    try:
        # Connect to Server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() # Secure the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True, "✅ OTP sent to your email!"
    except Exception as e:
        # FALLBACK FOR TESTING (If you haven't set up SMTP yet)
        print(f"========================================")
        print(f" [TEST MODE] OTP for {receiver_email}: {otp_code}")
        print(f" Error sending real email: {e}")
        print(f"========================================")
        return False, f"⚠️ Email failed (Check Console for OTP): {e}"
