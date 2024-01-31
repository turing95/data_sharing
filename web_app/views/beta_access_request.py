from web_app.forms import BetaAccessRequestForm
from django.views.generic.edit import FormView


class BetaAccessRequestFormView(FormView):
    template_name = "public/beta_access_request.html"
    form_class = BetaAccessRequestForm

    def form_valid(self, form):
        self.object = form.save()

        return self.render_to_response(self.get_context_data(form=form, submission_successful=True))
