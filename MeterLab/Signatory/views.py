import math
import datetime
import json
import json as json_util
from django.db import connection
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from .models import *
from .forms import *

from django.views.generic import CreateView, FormView, RedirectView, ListView

# Create your views here.


class Signs(FormView):
    form_class = signatoryForm
    success_url = '/'
    template_name = 'signatory/signatory.html'

    def form_valid(self, form):
        request = self.request
        sign = form.save(commit=False)
        sign.save()
        return super().form_valid(sign)


def Signatories(request):
    if request.method == "POST":
        id = request.POST['id']
        if id == 0:
            form = signatoryForm(request.POST)
        else:
            sign = signatory.objects.get(id=id)
            form = signatoryForm(request.POST, instance=sign)
        if form.is_valid():
            form.save()
        return redirect("../../")
    else:
        form = signatory.objects.get(pk=1)
        template_name = 'signatory/signatory.html'
        context = {'form': form, }
        return render(request, template_name, context)

