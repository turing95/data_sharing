from django.urls import reverse
from django.views.generic import ListView, FormView

from web_app.forms import CompanyForm
from web_app.mixins import CompanySideBarMixin, SubscriptionMixin, CompanyMixin
from web_app.models import Company
from django.utils.translation import gettext as _


class CompanyTabMixin:
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['company_tab'] = {
            'detail': {
                'active': False,  
                'alternative_text': _('Detail'),  
                'url_name': 'company_detail',  
                'svg_path': "M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z",  # SVG path for the icon
            },
            'contacts': {
                'active': False,  
                'alternative_text': _('Contacts'),  
                'url_name': 'company_contacts',  
                'svg_path': "M15 9h3.75M15 12h3.75M15 15h3.75M4.5 19.5h15a2.25 2.25 0 0 0 2.25-2.25V6.75A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25v10.5A2.25 2.25 0 0 0 4.5 19.5Zm6-10.125a1.875 1.875 0 1 1-3.75 0 1.875 1.875 0 0 1 3.75 0Zm1.294 6.336a6.721 6.721 0 0 1-3.17.789 6.721 6.721 0 0 1-3.168-.789 3.376 3.376 0 0 1 6.338 0Z",  # SVG path for the icon
            },
            'spaces': {
                'active': False,  
                'alternative_text': _('Spaces'),  
                'url_name': 'company_spaces', 
                'svg_path': "M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z",  # SVG path for the icon
            },
            'requests': {
                'active': False,  
                'alternative_text': _('Requests'),  
                'url_name': 'company_detail',  
                'svg_path': "M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z",  # SVG path for the icon
            },
            'documents': {
                'active': False,  
                'alternative_text': _('Documents'),  
                'url_name': 'company_detail',  
                'svg_path': "M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z",  # SVG path for the icon
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