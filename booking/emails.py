import hashlib
from django.core.mail import send_mail
from django.conf import settings

def generate_verification_code(email):
    # Encode the email address as UTF-8
    email = email.encode('utf-8')

    # Generate a SHA-256 hash of the email and take the first 5 characters
    m1 = hashlib.sha256(email).hexdigest()[:5]

    # Generate an MD5 hash of the email and take the first 3 characters
    m2 = hashlib.md5(email).hexdigest()[:3]

    # Convert the hexadecimal strings to integers and add them together
    verification_code = int(m1, 16) + int(m2, 16)

    # Print the verification code (for debugging purposes)
    print(verification_code)

    return verification_code

def send_verification_code(email):
    # Send an email with the verification code
    send_mail(
        subject='Verification Code',
        message=f'Hello from Booking System !!!\nYour verification code is {generate_verification_code(email)}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    return True
