from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.models import User


class CustomUser(User):
    class Meta:
        proxy = True

    def get_google_access_token(self):
        try:
            # Assuming 'google' is the provider name you have used with allauth
            social_account = SocialAccount.objects.get(user=self, provider='google')
            token = SocialToken.objects.get(account=social_account)
            return token.token  # token.token is the access token
        except SocialAccount.DoesNotExist:
            # Handle the case where the user does not have a Google social account
            return None
        except SocialToken.DoesNotExist:
            # Handle the case where the token does not exist
            return None
