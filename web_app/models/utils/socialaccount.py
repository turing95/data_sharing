from allauth.socialaccount import signals
from allauth.socialaccount.models import SocialAccount

from web_app.models import UploadRequest, GenericDestination


def disconnect_social_account(request, account):
    UploadRequest.objects.filter(destinations__social_account=account).update(is_active=False)
    GenericDestination.objects.filter(social_account=account).update(is_active=False)
    account.delete()
    signals.social_account_removed.send(
        sender=SocialAccount, request=request, socialaccount=account
    )
