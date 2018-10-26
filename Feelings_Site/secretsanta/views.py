from django.core import serializers
from django.views import View
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from secretsanta.forms import SignupForm


class SignupView(FormView):
    template_name = 'secretsanta/submissionform.html'
    form_class = SignupForm
    success_url = 'secretsanta/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(SignupView, self).form_valid(form)

class ThanksView(View):
    template_name = 'secretsanta/thanks.html'
    form_class = SignupForm
