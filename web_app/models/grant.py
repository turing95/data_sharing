from copy import deepcopy

from web_app.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Grant(BaseModel):
    class GrantStatus(models.TextChoices):
        ANNOUNCED = 'Announced', _('Announced')
        PUBLISHED = 'Published', _('Published')
        CLOSED = 'Closed', _('Closed')

    official_name = models.CharField(max_length=250, null=True,
                                     blank=True)  # full name of the grant like "Fabriq quarto 2020 innovazioni dei quartieri"
    name = models.CharField(max_length=250, null=True, blank=True)  # shorter version of name like "fabriq"
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='grants')
    space = models.OneToOneField('Space', on_delete=models.CASCADE, related_name='grant', null=True, blank=True)
    type = models.CharField(max_length=250, null=True, blank=True)
    tags = models.TextField(null=True, blank=True)  # comma separated list of tags
    status = models.CharField(
        max_length=50,
        choices=GrantStatus.choices,
        default=GrantStatus.ANNOUNCED)
    support_email = models.EmailField(null=True, blank=True)
    financer_name = models.CharField(max_length=250, null=True,
                                     blank=True)  # this will be substituted with a relation to a financer model
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
    de_minimis = models.BooleanField(default=False, null=True, blank=True)
    descriptive_other = models.TextField(null=True, blank=True)  # other notes generic field

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

    def duplicate_for_space(self, space):
        new_grant = deepcopy(self)
        new_grant.pk = None
        new_grant.space = space
        new_grant.save()
        for attachment in self.attachments.all():
            GrantAttachment.objects.create(grant=new_grant, file=attachment.file)
        for deadline in self.deadlines.all():
            GrantDeadline.objects.create(grant=new_grant, date=deadline.date, description=deadline.description,
                                         sender_visibility=deadline.sender_visibility)
        checklist = self.field_groups.filter(group=None).first()
        if checklist is not None:
            checklist.duplicate(grant=new_grant)
        return new_grant

    def to_space(self, user=None, space=None):
        from web_app.models import Space
        if space is None:
            space = Space.objects.create(title=self.name, organization=self.organization, user=user, grant=self)
        root_group = self.field_groups.filter(group=None).first()
        if root_group:
            root_group.to_request(space, label=self.name)
        return space

class GrantAttachment(BaseModel):
    file = models.OneToOneField('File', on_delete=models.CASCADE, related_name='grant_attachment')
    grant = models.ForeignKey('Grant', on_delete=models.CASCADE, related_name='attachments')


class GrantDeadline(BaseModel):
    grant = models.ForeignKey('Grant', on_delete=models.CASCADE, related_name='deadlines')
    date = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    sender_visibility = models.BooleanField(default=False)
