from django.urls import reverse
from django.views.generic import ListView, FormView

from web_app.forms import CompanyForm
from web_app.mixins import CompanySideBarMixin, SubscriptionMixin, CompanyMixin
from web_app.models import Company
from django.utils.translation import gettext as _
from web_app.utils.svg_icon_paths import svg_icons_path as paths


class CompanyTabMixin:
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['company_tab'] = {
            'detail': {
                'active': False,  
                'alternative_text': _('Detail'),  
                'url_name': 'company_detail',  
                'svg_path': paths['detail']
            },
            'contacts': {
                'active': False,  
                'alternative_text': _('Contacts'),  
                'url_name': 'company_contacts',  
                'svg_path': paths['contacts']
            },
            'spaces': {
                'active': False,  
                'alternative_text': _('Spaces'),  
                'url_name': 'company_spaces', 
                'svg_path': paths['spaces']
            },
            'requests': {
                'active': False,  
                'alternative_text': _('Requests'),  
                'url_name': 'company_detail',  
                'svg_path': paths['requests']
            },
            
            'documents': {
                'active': False,  
                'alternative_text': _('Documents'),  
                'url_name': 'company_detail',  
                'svg_path': paths['documents']
            },

        }
        return data



class CompanyDetailView(SubscriptionMixin, CompanySideBarMixin, CompanyTabMixin, CompanyMixin, FormView):
    template_name = "private/company/detail/base.html"
    form_class = CompanyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_tab']['detail']['active'] = True
        '''context['back'] = {'url': reverse_lazy('companies', kwargs={'organization_uuid': self.get_company().organization.pk}),
                        'text': 'Back to Companies'}'''
        return context

    def get_success_url(self):
        return reverse('companies', kwargs={'organization_uuid': self.get_company().organization.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_company()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CompanySpacesListView(SubscriptionMixin, CompanySideBarMixin, CompanyTabMixin, CompanyMixin, ListView):
    template_name = "private/company/detail/spaces_list.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_tab']['spaces']['active'] = True
        return context

    def get_queryset(self):
        return self.get_company().spaces.filter(is_deleted=False).order_by('created_at')
    
class CompanyContactsListView(SubscriptionMixin, CompanySideBarMixin, CompanyTabMixin, CompanyMixin, ListView):
    template_name = "private/company/detail/contacts_list.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_tab']['contacts']['active'] = True
        return context

    def get_queryset(self):
        return self.get_company().spaces.filter(is_deleted=False).order_by('created_at')