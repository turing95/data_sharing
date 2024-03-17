from copy import deepcopy

from django.db import models
from django.urls import reverse

from web_app.models import BaseModel, DeleteModel
from django.conf import settings
import pytz
import arrow


class Space(BaseModel):
    TIMEZONE_CHOICES = tuple((tz, tz) for tz in pytz.all_timezones)

    title = models.CharField(max_length=250)
    user = models.ForeignKey('User', null=True, on_delete=models.SET_NULL, related_name='spaces')
    organization = models.ForeignKey('Organization', null=True, on_delete=models.CASCADE, related_name='spaces')
    company = models.ForeignKey('Company', null=True, on_delete=models.SET_NULL, related_name='spaces')
    is_public = models.BooleanField(default=False)
    instructions = models.TextField(null=True, blank=True)
    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES
    )
    locale = models.CharField(max_length=10, null=True, blank=True, default='en-us')

    @property
    def has_complete_requests(self):
        return any(req.is_complete for req in self.requests.all())

    @property
    def has_incomplete_requests(self):
        return any(not req.is_complete for req in self.requests.all())


    @property
    def link_for_email(self):
        return settings.BASE_URL + reverse('receiver_space_detail', kwargs={
            'space_uuid': self.uuid
        })

    @property
    def sections_position_sorted(self):
        return self.sections.order_by('position')
    
    def add_section(self, text_section=None, file_section=None, prev_section_position=None):
        from web_app.models import SpaceSection
        if prev_section_position:
            inserting_position = int(prev_section_position) + 1
        else:
            inserting_position = 1
        # increase by 1 all the positions of the sections that have a position greater than or equal to the inserting position
        self.sections.filter(position__gte=inserting_position).update(
            position=models.F('position') + 1)
        space_section = SpaceSection.objects.create(space=self, file_section=file_section,
                                                    text_section=text_section,
                                                    position=inserting_position)
        

    def setup(self):
        from web_app.models import GenericDestination, Kezyy
        GenericDestination.create_provider(Kezyy.TAG,
                                           self.user, space=self)

    def title_form(self,request_post=None):
        from web_app.forms import SpaceTitleForm
        return SpaceTitleForm(request_post,instance=self)

    def duplicate(self, user):
        #TODO fix
        new_space = deepcopy(self)
        new_space.pk = None
        new_space.user = user
        new_space.title = f'{self.title} (copy)'
        new_space.save()
        for sender in self.senders.all():
            sender.duplicate(new_space)

        for request in self.requests.all().order_by('created_at'):
            request.duplicate(new_space)
        return new_space



    class Meta:
        ordering = ['-created_at']
