from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template

from .forms import ExaminationForm


class ExaminationView(FormView):
    template_name = "exam.html"
    form_class = ExaminationForm
    success_url = reverse_lazy("/")

    def form_valid(self, form, **kwargs):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        context = self.get_context_data(**kwargs)
        result = form.predict_loan_status()
        context['predictedLabel'] = result['predictedLabel']
        return self.render_to_response(context)
