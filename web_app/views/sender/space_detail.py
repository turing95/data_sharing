from django.shortcuts import get_object_or_404

from web_app.forms import SpaceDetailForm
from django.views.generic.edit import FormView
from web_app.models import Space, GenericDestination, GoogleDrive
from django.urls import reverse_lazy
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django import forms
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken, SocialAccount


class SpaceDetailFormView(FormView):
    template_name = "sender/space_detail.html"
    form_class = SpaceDetailForm
    success_url = reverse_lazy('spaces')
    _space = None

    def form_valid(self, form):
        space = self.get_space()
        requests = space.requests.all() if self.kwargs.get('sender_uuid',None) is not None else space.requests.filter(senders__uuid=self.kwargs.get('sender_uuid'))
        for space_req in requests:
            field_name = f'file_{space_req.pk}'
            uploaded_file = form.cleaned_data.get(field_name)
            if uploaded_file:
                # Use the stored access token
                google_drive_destination: GoogleDrive = GenericDestination.objects.get(request=space_req).related_object

                social_account = SocialAccount.objects.get(user=space.user)
                access_token = SocialToken.objects.get(account=social_account).token

                credentials = Credentials(token=access_token)

                # Build the Drive service
                service = build('drive', 'v3', credentials=credentials)

                # File to be uploaded
                temp_file_path = default_storage.save("temp/" + uploaded_file.name, ContentFile(uploaded_file.read()))
                full_file_path = default_storage.path(temp_file_path)

                # File to be uploaded
                file_metadata = {'name': space_req.file_name or uploaded_file.name,
                                 'parents': [google_drive_destination.folder_id]}
                media = MediaFileUpload(full_file_path,
                                        mimetype=uploaded_file.content_type)

                # Upload the file
                file = service.files().create(body=file_metadata,
                                              media_body=media,
                                              fields='id').execute()
                print(file)
        return super().form_valid(form)

    def get_space(self):
        if not self._space:
            space_uuid = self.kwargs.get('space_uuid')
            sender_uuid = self.kwargs.get('sender_uuid',None)
            if sender_uuid:
                self._space = get_object_or_404(Space, pk=space_uuid, is_active=True,is_public = False, requests__senders__uuid=sender_uuid)
            else:
                self._space = get_object_or_404(Space, pk=space_uuid, is_public=True, is_active=True)
        return self._space

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        space: Space = self.get_space()

        for index, space_req in enumerate(space.requests.all()):
            form.fields[f'file_{space_req.pk}'] = forms.FileField()

        return form
