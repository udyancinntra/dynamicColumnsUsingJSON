
from email.message import EmailMessage
import os
from django.http import HttpResponse


email = EmailMessage(
    'Subject of mail sent by Django',
    'Content of mail sent by Django',
    'guptaudyan1@gmail.com',
    ['guptaudyan1@gmail.com']
)

 # Path to the .txt file to be attached
file_path = os.path.join(os.path.dirname(__file__), 'sample.txt')  # put file in same level as views.py
if os.path.exists(file_path):
    email.attach_file(file_path)
    
try:
    email.send()
    print("Email sent successfully")
except Exception as e:
    print(f"Failed to send email: {e}")