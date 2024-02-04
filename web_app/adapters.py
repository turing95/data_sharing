from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.urls import reverse

from web_app.models import Organization


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
        print(user)
        # Check if an organization named "Personal" already exists in the user's organizations
        personal_organization_exists = user.organizations.filter(name="Personal").exists()

        # If it does not exist, create it and add it to the user's organizations
        if not personal_organization_exists:
            personal_organization = Organization.objects.create(name="Personal")
            user.organizations.add(personal_organization)

        return user
