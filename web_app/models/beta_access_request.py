from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.db import models
from web_app.models import BaseModel


class BetaAccessRequest(BaseModel):
    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    industry = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)
    user_role = models.CharField(max_length=50, null=True, blank=True)
    intended_use = models.TextField(null=True, blank=True)
    first_touchpoint = models.CharField(max_length=150, null=True, blank=True)

    def notify(self):
        txt = f"""
        New beta access request from {self.user_name} ({self.user_email})
        Industry: {self.industry}
        Country: {self.country}
        Company: {self.company}
        User role: {self.user_role}
        Intended use: {self.intended_use}
        First touchpoint: {self.first_touchpoint}
        """

        with get_connection(
                host=settings.RESEND_SMTP_HOST,
                port=settings.RESEND_SMTP_PORT,
                username=settings.RESEND_SMTP_USERNAME,
                password=settings.RESEND_API_KEY,
                use_tls=True,
        ) as connection:
            msg = EmailMultiAlternatives(
                subject=f'New beta access request from {self.user_name} ({self.user_email})',
                body=txt,
                from_email=settings.NO_REPLY_EMAIL,
                to=['beta@kezyy.com'],
                reply_to=[settings.NO_REPLY_EMAIL],
                connection=connection,
                headers={'Return-Path': settings.NO_REPLY_EMAIL}
            )
            msg.attach_alternative(txt, 'text/html')
            msg.send()

            return True
