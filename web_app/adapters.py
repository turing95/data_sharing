from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string

from django.utils.translation import gettext_lazy as _

from utils.emails import html_to_text


class AccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        ctx = {
            "current_site": settings.BASE_URL,
        }
        ctx.update(context)
        email_html = render_to_string('emails/password_reset.html', ctx)
        from_email = f"Kezyy <{settings.NO_REPLY_EMAIL}>"
        with get_connection(
                host=settings.RESEND_SMTP_HOST,
                port=settings.RESEND_SMTP_PORT,
                username=settings.RESEND_SMTP_USERNAME,
                password=settings.RESEND_API_KEY,
                use_tls=True,
        ) as connection:
            msg = EmailMultiAlternatives(
                subject=_('Reset Password'),
                body=html_to_text(email_html),
                from_email=from_email,
                to=[email],
                reply_to=[from_email],
                connection=connection,
                headers={'Return-Path': from_email}
            )
            msg.attach_alternative(email_html, 'text/html')

            msg.send()

    def save_user(self, request, user, form, commit=True):
        # Call the super class's save_user to save the user model
        user = super().save_user(request, user, form, commit=True)
        user.setup(request)

        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def validate_disconnect(self, account, accounts):
        if len(accounts) == 1:
            messages.error(self.request, _("You can not disconnect from your last account"))
            raise ValidationError(_("Cannot disconnect"))

    def save_user(self, request, user, form=None):
        # Call the super class's save_user to save the user model
        user = super().save_user(request, user, form)
        user.setup(request)

        return user
