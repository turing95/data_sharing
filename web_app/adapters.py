from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.urls import reverse

from web_app.models import Organization, SenderNotificationsSettings


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        if request.path.rstrip("/") == reverse("account_signup").rstrip("/"):
            return False
        return True


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def validate_disconnect(self, account, accounts):
        if len(accounts) == 1:
            messages.error(self.request, "You can not disconnect from your last account")
            raise ValidationError("Can not disconnect")

    def save_user(self, request, user, form=None):
        # Call the super class's save_user to save the user model
        user = super().save_user(request, user, form)
        user.setup()

        return user
