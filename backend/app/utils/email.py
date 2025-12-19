"""
Email Sending Utilities.

Provides functions for sending emails to users.
Currently uses a mock implementation that prints to console.

TODO: Integrate with a real email service provider:
- SendGrid (https://sendgrid.com/)
- AWS SES (https://aws.amazon.com/ses/)
- Mailgun (https://www.mailgun.com/)
- Postmark (https://postmarkapp.com/)
"""

import os
from typing import Optional


def send_password_reset_email(email: str, reset_token: str, user_name: Optional[str] = None) -> None:
    """
    Send password reset email to user.

    For development/testing, this prints the email to console.
    In production, replace with actual email service integration.

    Args:
        email: User's email address
        reset_token: Password reset token
        user_name: Optional user name for personalization

    Example:
        >>> send_password_reset_email("user@example.com", "abc123token")
        # Prints mock email to console

    Production Implementation Example (SendGrid):
        ```python
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail

        message = Mail(
            from_email='noreply@roof.com',
            to_emails=email,
            subject='Reset Your Password - Roof',
            html_content=email_html
        )

        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(f"Email sent! Status: {response.status_code}")
        except Exception as e:
            print(f"Error sending email: {e}")
        ```
    """
    # Construct reset URL
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    reset_url = f"{frontend_url}/reset-password?token={reset_token}"

    # Personalize greeting
    greeting = f"Hi {user_name}," if user_name else "Hi,"

    # Mock: Print to console (replace with actual email sending in production)
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║           PASSWORD RESET EMAIL (MOCK - CONSOLE OUTPUT)       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  To: {email:<55} ║
║  Subject: Reset Your Password - Roof                        ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣

{greeting}

You requested a password reset for your Roof account.

Click the link below to create a new password:

🔗 {reset_url}

⏰ This link will expire in 24 hours.

If you didn't request this password reset, please ignore this email.
Your password will remain unchanged.

For security reasons, never share this link with anyone.

---
Need help? Contact support@roof.com

Roof Team
╚══════════════════════════════════════════════════════════════╝
""")

    # Log the email send (in production, log to file or logging service)
    print(f"[EMAIL LOG] Password reset email sent to: {email}")


def send_password_reset_confirmation(email: str, user_name: Optional[str] = None) -> None:
    """
    Send confirmation email after successful password reset.

    Args:
        email: User's email address
        user_name: Optional user name for personalization

    Example:
        >>> send_password_reset_confirmation("user@example.com", "John")
    """
    greeting = f"Hi {user_name}," if user_name else "Hi,"

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║      PASSWORD RESET CONFIRMATION (MOCK - CONSOLE OUTPUT)     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  To: {email:<55} ║
║  Subject: Your Password Was Reset - Roof                    ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣

{greeting}

✅ Your password has been successfully reset.

You can now log in to your Roof account using your new password.

If you didn't make this change, please contact our support team
immediately at support@roof.com.

For your security, we recommend:
• Using a strong, unique password
• Enabling two-factor authentication (coming soon!)
• Never sharing your password with anyone

---
Roof Team
╚══════════════════════════════════════════════════════════════╝
""")

    print(f"[EMAIL LOG] Password reset confirmation sent to: {email}")


# TODO: Production email implementation template
"""
# Install SendGrid:
# pip install sendgrid

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_via_sendgrid(to_email: str, subject: str, html_content: str):
    '''Send email using SendGrid API.'''
    message = Mail(
        from_email=('noreply@roof.com', 'Roof'),
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)

        if response.status_code == 202:
            print(f"Email sent successfully to {to_email}")
            return True
        else:
            print(f"Email send failed with status: {response.status_code}")
            return False

    except Exception as e:
        print(f"Error sending email: {e}")
        return False
"""
