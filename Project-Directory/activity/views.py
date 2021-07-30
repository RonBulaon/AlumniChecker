from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views import generic

from scanner.models import Visitor, Visit
from scanner.models import Configuration

from django.contrib.auth.decorators import login_required
from app1.decorators import allowed_users

from .filters import VisitsFilter
from app1.models import SiteWide

@login_required(login_url='login')
@allowed_users(allowed_roles=['adminGroup'])
def filteredVisits(request):
    qs = Visit.objects.all().order_by('-date')
    barcode_contains_query = request.GET.get('barcode','')
    name_contains_query = request.GET.get('name','')
    email_contains_query = request.GET.get('email','')
    page = request.GET.get('page', 1)

    qs =qs.filter(barcode__icontains=barcode_contains_query) \
        .filter(name__icontains=name_contains_query) \
        .filter(email__icontains=email_contains_query) 
   
    currentValue = {
        'barcode':request.GET.get('barcode'),
        'name':request.GET.get('name'),
        'email':request.GET.get('email')
    }
    count = int(Configuration.objects.values('visits_pagination').first()['visits_pagination'])
    paginator = Paginator(qs, count)
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    sitewide = SiteWide.objects.all().first()
    context = {
        'qs' : qs,
        'currentValue' : currentValue,
        'sitewide' : sitewide
    }

    return render(request, 'activity/filteredVisits.html', context)