from web_app.forms import BetaAccessRequestForm
from web_app.models import BetaAccessRequest
from django.views.generic.edit import FormView
from web_app.tasks.notifications import notify_beta_access_request


class BetaAccessRequestFormView(FormView):
    template_name = "public/beta_access_request.html"
    form_class = BetaAccessRequestForm
    
    #set context beta acess form to true
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['beta_access_form'] = True
        return context

    def form_valid(self, form):
        self.beta_access_req: BetaAccessRequest = form.save()
        notify_beta_access_request.delay(self.beta_access_req.pk)
        return self.render_to_response(self.get_context_data(form=form, submission_successful=True))
