import hashlib
from django.core.mail import send_mail
from django.conf import settings

def generate_verification_code(email):
    email = email.encode('utf-8')
    m1 = hashlib.sha256(email).hexdigest()[:5]
    m2 = hashlib.md5(email).hexdigest()[:3]
    print(int(m1, 16) + int(m2, 16))
    return int(m1, 16) + int(m2, 16)

def sendverificationcode(email):
    send_mail(
        subject='Verification Code',
        message=f'Hello from Booking System !!!\nYour verification code is {generate_verification_code(email)}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    return True
