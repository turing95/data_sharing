from web_app.forms import BetaAccessRequestForm
from django.views.generic.edit import FormView


class BetaAccessRequestFormView(FormView):
    template_name = "public/beta_access_request.html"
    form_class = BetaAccessRequestForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure 'submission_success' is in context and set to False by default
        if 'submission_successful' not in context:
            context['submission_successful'] = False
        return context

   
    def form_valid(self, form):
        self.object = form.save()
        
        return self.render_to_response(self.get_context_data(form=form, submission_successful=True))
