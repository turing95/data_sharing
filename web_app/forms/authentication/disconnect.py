from allauth.socialaccount.forms import DisconnectForm


class CustomSocialDisconnectForm(DisconnectForm):

    def save(self):
        # Add your own processing here if you do need access to the
        # socialaccount being deleted.

        # Ensure you call the parent class's save.
        # .save() does not return anything
        super(CustomSocialDisconnectForm, self).save()

        # Add your own processing here if you don't need access to the
        # socialaccount being deleted.
