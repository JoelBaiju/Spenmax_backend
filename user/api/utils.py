from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
import random
import string

def send_confirmation_email(applicant_email, applicant_name):
    subject = "Account has Created in Kriado"
    html_content = render_to_string(
        'UserEmail.html',
        {
            'applicant_name': applicant_name,
        }
    )
    send_mail(
        subject,
        '',
        # From email address (can be None or your sender address)
        settings.EMAIL_HOST_USER,
        [applicant_email],  # To email address
        html_message=html_content,
    )


def generate_random_password():
    # Define the characters to use for generating the password
    characters = string.ascii_letters + string.digits

    # Generate a random password with 8 characters
    password = ''.join(random.choice(characters) for _ in range(8))

    return "123456"


def send_verification_email(applicant_email, applicant_name,hassed_email):
    subject = "Account has to verify"
    html_content = render_to_string(
        'UserVerify.html',
        {
            'applicant_name': applicant_name,
            'hassed_email': hassed_email,
        }
    )
    send_mail(
        subject,
        '',
        # From email address (can be None or your sender address)
        settings.EMAIL_HOST_USER,
        [applicant_email],  # To email address
        html_message=html_content,
    )

def send_forgotverificaiton_email(applicant_email,hassed_email):
    subject = "Account has to verify"
    html_content = render_to_string(
        'Userforgot.html',
        {
            'hassed_email': hassed_email,
        }
    )
    send_mail(
        subject,
        '',
        # From email address (can be None or your sender address)
        settings.EMAIL_HOST_USER,
        [applicant_email],  # To email address
        html_message=html_content,
    )

def sendOTP(email):

    otp = str(random.randint(1000, 9999))
    subject = f"Your One-Time Password (OTP)"
    message = f"Your One-Time Password (OTP) for Spenmax to reset password is {otp}"


    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    return otp
