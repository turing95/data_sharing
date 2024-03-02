from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView
from web_app.mixins import OrganizationMixin, SubscriptionMixin, SideBarMixin
from web_app.forms import TeamInviteForm
from web_app.models import Organization, OrganizationInvitation, User, UserOrganization


class TeamSideBarMixin(SideBarMixin):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sidebar']['team'] = True
        return data


class TeamView(SubscriptionMixin, OrganizationMixin, TeamSideBarMixin, ListView):
    template_name = "private/organization/team_list.html"
    paginate_by = 12

    def get_queryset(self):
        return self.get_organization().userorganization_set.all().order_by('created_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['invite_form'] = TeamInviteForm()
        context['invitations'] = OrganizationInvitation.objects.filter(organization=self.get_organization(),
                                                                       invited_by=self.request.user)
        return context


@require_POST
@login_required
def team_invitation(request, organization_uuid):
    if request.method == 'POST':
        organization = Organization.objects.get(pk=organization_uuid, users=request.user)
        form = TeamInviteForm(request.POST, organization=organization)
        if form.is_valid():
            organization.invite_user(form.cleaned_data['email'], request.user)
            messages.success(request, 'User invited successfully')
            return redirect(reverse('team', kwargs={'organization_uuid': organization.pk}))
        messages.error(request, form.errors['email'])
        return redirect(reverse('team', kwargs={'organization_uuid': organization.pk}))
    return HttpResponseBadRequest()


@require_GET
def team_invitation_redemption(request):
    if request.method == 'GET':
        token = request.GET.get('token', None)
        if not token:
            return HttpResponseNotFound()
        invitation = get_object_or_404(OrganizationInvitation, token=token)
        user = User.objects.filter(email=invitation.email).first()
        if user:
            invitation.organization.users.add(user)
            invitation.delete()
            messages.success(request, 'User added to organization successfully')
            return redirect(reverse('spaces'), kwargs={'organization_uuid': invitation.organization.pk})
        else:
            request.session['invitation_uuid'] = str(invitation.pk)
            request.session['invitation_email'] = invitation.email
            return redirect(reverse("account_signup"))
    return HttpResponseNotFound()


@require_POST
@login_required
def revoke_invitation(request, invitation_uuid):
    invitation = get_object_or_404(OrganizationInvitation, pk=invitation_uuid)
    if invitation.invited_by == request.user:
        invitation.delete()
        messages.success(request, 'Invitation revoked successfully')
        return redirect(reverse('team', kwargs={'organization_uuid': invitation.organization.pk}))
    return HttpResponseNotFound()


@require_POST
@login_required
def remove_team_member(request, user_org_uuid):
    user_org = UserOrganization.objects.get(pk=user_org_uuid)
    organization_uuid = user_org.organization.pk
    user = user_org.user
    user_org.delete()
    if user == request.user:
        messages.success(request, 'You have left the organization')
        return redirect(reverse('spaces'))
    messages.success(request, 'User removed from organization')
    return redirect(reverse('team', kwargs={'organization_uuid': organization_uuid}))
