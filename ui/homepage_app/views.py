from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import requests 

from .utils import get_service_registry_context

# Create your views here.
def index(request):

    # Fetch the Service Registry information as a context dict
    serviceRegistryUrl = ""
    context = get_service_registry_context(serviceRegistryUrl)

    return render(request, 'homepage/index.html', context)