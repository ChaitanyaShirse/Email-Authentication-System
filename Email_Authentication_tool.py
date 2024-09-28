import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import dns.resolver
import smtplib
import socket

# Check if the email has a valid format
def is_valid_format(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Check if the email domain has valid MX records (used for mail delivery)
def has_valid_domain(email):
    try:
        domain = email.split('@')[1]
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return False

# Check if the email exists using SMTP validation
def email_exists(email):
    domain = email.split('@')[1]
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange)

        # SMTP handshake
        with smtplib.SMTP(mx_record, timeout=10) as server:
            server.set_debuglevel(0)
            server.helo()
            server.mail('your-email@example.com')  # Replace with your sender email
            code, _ = server.rcpt(email)  # Send recipient's email
        return code == 250  # 250 means the recipient exists
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, socket.error, smtplib.SMTPException):
        return False

# Simple spam check: Basic heuristic with spammy domains
def is_spam_email(email):
    spammy_domains = ["spamdomain.com", "tempmail.com", "fakemail.net", "spammail.org", "spammail.in"]
    domain = email.split('@')[1]
    return domain in spammy_domains

# Function to check if the email is real, fake, or spam
def check_email():
    email = email_entry.get()

    if not is_valid_format(email):
        messagebox.showinfo("Result", "Invalid email format", icon="warning")
        return
    
    if not has_valid_domain(email):
        messagebox.showinfo("Result", "Invalid email domain", icon="warning")
        return
    
    if is_spam_email(email):
        messagebox.showinfo("Result", "This email is flagged as SPAM", icon="warning")
        return
    
    if not email_exists(email):
        messagebox.showinfo("Result", "The email does not exist", icon="warning")
        return
    
    messagebox.showinfo("Result", "The email looks real and exists", icon="info")

# Create the enhanced GUI window
window = tk.Tk()
window.title("Email Verification Tool")
window.geometry("900x500")

# Load background image
bg_image = Image.open("D:\PYTHON\Images\mail.jpg")  # Update with the path to your image
#bg_image = bg_image.resize((900, 500), Image.ANTIALIAS)  # Resize image to fit the window
bg_photo = ImageTk.PhotoImage(bg_image)

# Set background image as a label
bg_label = tk.Label(window, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Cover the entire window

# Header Label (centered)
header_label = tk.Label(window, text="Email Verification Tool", font=("Arial", 24, "bold"), fg="#7A007A", bg="white")
header_label.place(relx=0.5, y=80, anchor="center")  # Centered at the top

# Email Input Label
label = tk.Label(window, text="Enter Email:", font=("Arial", 16, "bold"), fg="orange", bg="#f0f0f0")
label.place(x=120, y=180)

# Email Entry Field
email_entry = tk.Entry(window, width=35, font=("Arial", 16), bg="#f0f0f0")
email_entry.place(x=250, y=180)

# Check Email Button (centered)
def on_enter(e):
    check_button['background'] = '#45a049'  # Lighter green on hover

def on_leave(e):
    check_button['background'] = '#4CAF50'  # Default green

check_button = tk.Button(window, text="Check Email", command=check_email, bg="#4CAF50", fg="white", font=("Arial", 16), width=20)
check_button.place(relx=0.5, rely=0.6, anchor="center")  # Centered horizontally

check_button.bind("<Enter>", on_enter)  # Hover effect
check_button.bind("<Leave>", on_leave)

# Footer Label (centered at bottom)
footer_label = tk.Label(window, text="Developed by Chaitanya Shirse", font=("Arial", 12), fg="yellow", bg="#282828")
footer_label.place(relx=0.5, rely=0.95, anchor="center")

# Run the application
window.mainloop()
