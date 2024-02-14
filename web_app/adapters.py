from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
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

    def pre_social_login(self, request, sociallogin):
        # Assuming 'sociallogin' is the social login attempt being processed
        # Check if the user is authenticated and the social account is not already linked
        if request.user.is_authenticated:
            existing_social_accounts = SocialAccount.objects.filter(provider=sociallogin.account.provider,
                                                                    user=request.user)
            if existing_social_accounts.exists():
                # Here you would handle the case where the user already has a social account for this provider
                # For example, you could redirect to a custom error page or display an error message
                # This is a placeholder for how you might start a redirect; adjust as necessary for your application
                provider = self.get_provider(request, sociallogin.account.provider)
                messages.error(request, f"You already have an account with {provider.name}, reconnect or disconnect the existing one.")
                return redirect(request.get_full_path())
    def save_user(self, request, user, form=None):
        # Call the super class's save_user to save the user model
        user = super().save_user(request, user, form)
        # Check if an organization named "Personal" already exists in the user's organizations
        SenderNotificationsSettings.objects.get_or_create(user=user)
        personal_organization_exists = user.organizations.filter(name="Personal").exists()

        # If it does not exist, create it and add it to the user's organizations
        if not personal_organization_exists:
            personal_organization = Organization.objects.create(name="Personal")
            user.organizations.add(personal_organization)

        return user
