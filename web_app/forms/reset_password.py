from allauth.account.forms import ResetPasswordForm as AllauthResetPasswordForm
from web_app.forms.css_classes.inputs import text_input, text_input_label

class ResetPasswordForm(AllauthResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)            
            
        # Set placeholder for the email field
        self.fields['email'].widget.attrs.update({
            'placeholder': 'myemail@mail.com',
            'class': text_input  
        })
