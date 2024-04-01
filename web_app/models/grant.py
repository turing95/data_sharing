from web_app.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Grant(BaseModel):
    class GrantStatus(models.TextChoices):
        ANNOUNCED = 'Announced', _('Announced')
        PUBLISHED = 'Published', _('Published')
        CLOSED = 'Closed', _('Closed')
    
    official_name = models.CharField(max_length=250, null=True, blank=True) # full name of the grant like "Fabriq quarto 2020 innovazioni dei quartieri"
    name = models.CharField(max_length=250, null=True, blank=True) # shorter version of name like "fabriq"
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='grants')
    type = models.CharField(max_length=250, null=True, blank=True)
    tags = models.TextField(null=True, blank=True) # comma separated list of tags
    status = models.CharField(
                    max_length=50,
                    choices=GrantStatus.choices,
                    default=GrantStatus.ANNOUNCED)
    support_email = models.EmailField(null=True, blank=True)
    financer_name = models.CharField(max_length=250, null=True, blank=True) # this will be substituted with a relation to a financer model
    financer_website_link = models.URLField(null=True, blank=True)
    descriptive_timeline = models.TextField(null=True, blank=True)
    descriptive_beneficiaries = models.TextField(null=True, blank=True)
    descriptive_goals = models.TextField(null=True, blank=True)
    descriptive_funds = models.TextField(null=True, blank=True)
    descriptive_allowed_activities = models.TextField(null=True, blank=True)
    descriptive_admitted_expenses = models.TextField(null=True, blank=True)
    descriptive_not_admitted_expenses = models.TextField(null=True, blank=True)
    descriptive_application_iter = models.TextField(null=True, blank=True)
    official_page_link = models.URLField(null=True, blank=True)
    application_page_link = models.URLField(null=True, blank=True)
    de_minimis = models.BooleanField(default=False)
    descriptive_other = models.TextField(null=True, blank=True) # other notes generic field
    
    
    # timeline with milestones
    # attachments
    # checklist (company like fields)
    # tags
    # it will be needed a non descriptive version of the allowed expenses, activities, beneficiaries, 
    # some way to manage updates (like new attachments of changes to the rules)
    
    def name_form(self, request_post=None):
        from web_app.forms import GrantNameForm
        return GrantNameForm(request_post, instance=self)

    def form(self, request_post=None):
        from web_app.forms import GrantForm
        return GrantForm(request_post, instance=self, organization=self.organization)