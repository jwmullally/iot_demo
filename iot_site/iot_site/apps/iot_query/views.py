from django.shortcuts import render

from . import models

# Create your views here.

def query(request):
    if request.GET:
        form = models.QueryForm(request.user, request.GET)
    else:
        form = models.QueryForm(request.user)
    context = {
            'form': form,
            'query_params': request.GET.urlencode(),
            }
    return render(request, 'iot_query/query.html', context)
