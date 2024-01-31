from django.forms import ModelForm
from web_app.models import BetaAccessRequest
from web_app.forms import css_classes
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class BetaAccessRequestForm(ModelForm):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'John Doe',
                                                             'class': css_classes.text_input}),
                            label='User Name',
                            help_text="")
    
    user_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'jhon.doe@mail.com',
                                                             'class': css_classes.text_input}),
                            
                            label='User Email',
                            help_text="This email will be used to grant you access to the beta version, pay attention to the spelling or you will not hear from us.")
    
    industry = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Finance',
                                                             'class': css_classes.text_input}),
                            required=False,
                            label='Industry',
                            help_text="")
    
    country = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'United States',
                                                             'class': css_classes.text_input}),
                            required=False,
                            label='Country',
                            help_text="")
    
    company = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Acme Inc.',
                                                             'class': css_classes.text_input}),
                            required=False,
                            label='Company',
                            help_text="")
    
    user_role = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Accountant',
                                                             'class': css_classes.text_input}),
                            required=False,
                            label='Role',
                            help_text="")      

    
    intended_use = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Explain what you would like to use Kezyy for',
            'rows': 3,
            'class': css_classes.text_area,
        }),
        label='Intended use',
        help_text=""" """)
        
    first_touchpoint = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Linkedin',
                                                             'class': css_classes.text_input}),
                            required=False,
                            label='First Touchpoint',
                            help_text="")
    
    checker = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'come at me bro',
                                                            'class': "hidden"}),
                        required=False,
                        label='are you a bot?',
                        help_text="")    

    class Meta:
        model = BetaAccessRequest
        fields = ['user_name', 'user_email', 'industry', 'country', 'company', 'user_role', 'intended_use', 'first_touchpoint']

        
    def clean_user_email(self):
        email = self.cleaned_data.get('user_email', None)
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(f"{email} is not a valid email address")
        return email
    
    def clean_checker(self):
        checker = self.cleaned_data.get('checker', None)
        if checker != "":
            raise ValidationError(f"Are you a bot?")
        return checker
            
