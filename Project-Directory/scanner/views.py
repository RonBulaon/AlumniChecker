from django.shortcuts import render, get_object_or_404
from django.contrib import messages

import datetime as dt 

from .alma_api import getAlmaRecords
from app1.models import SiteWide
from .models import Visitor, Visit, PeakHours

from django.contrib.auth.decorators import login_required
from app1.decorators import allowed_users

@login_required(login_url='login')
@allowed_users(allowed_roles=['userGroup', 'adminGroup'])
def scanner(request):
    sitewide = SiteWide.objects.all().first()
    return render(request, 'scanner/scanner.html', { 'sitewide':sitewide })


def peak():   
    current_hour = dt.datetime.now().hour
    if PeakHours.objects.filter(hour=current_hour).count() >= 1:
        return True
    else:
        return False


def visitor(request):
    sitewide = SiteWide.objects.all().first()
    return render(request, 'scanner/visitor.html', { 'sitewide':sitewide })


def error(request):
    return render(request, 'scanner/error.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['userGroup', 'adminGroup'])
def visitor(request, barcode):
    try:
        alma_userinfo = getAlmaRecords(barcode)

        if alma_userinfo['name'] and alma_userinfo['email']: 
            membership_info = 'Alumni'
        else:
            membership_info = 'Graduated SMU Student'
    except:
        return render(request, 'scanner/error.html')
    else:
        try:
            obj = Visitor.objects.get(barcode=barcode)

            if alma_userinfo['name'] != '':
                if Visitor.objects.filter(barcode=barcode).values("name") != alma_userinfo['name']:
                    Visitor.objects.filter(barcode=barcode).update(name=alma_userinfo['name'])

            if alma_userinfo['email'] != '':
                if Visitor.objects.filter(barcode=barcode).values("email") != alma_userinfo['email']:
                    Visitor.objects.filter(barcode=barcode).update(email=alma_userinfo['email'])

        except Visitor.DoesNotExist:
            obj = Visitor(name=alma_userinfo['name'], \
                                    email=alma_userinfo['email'], \
                                    barcode=barcode)
            obj.save()

    if membership_info == 'Alumni':
        obj2 = Visit.objects.create(
            barcode=barcode,\
            membership=membership_info,\
            status='True',\
            name=alma_userinfo['name'], \
            email=alma_userinfo['email']

        )
        messages.success(request, "Welcome to SMU Libraries! Entry Recorded!")
        

    elif membership_info == 'Graduated SMU Student' and peak() == False:
        obj2 = Visit.objects.create(
            barcode=barcode,\
            membership=membership_info,\
            status='True', \
            name=alma_userinfo['name'], \
            email=alma_userinfo['email']
        )
        messages.success(request, "Welcome to SMU Libraries! Entry Recorded!")

    else:
        obj2 = Visit.objects.create(
            barcode=barcode,\
            membership=membership_info,\
            status='False',
            name=alma_userinfo['name'], \
            email=alma_userinfo['email']
        )
        messages.error(request, "Not Allowed! Attempt Recorded. Please visit during non-peak hours!")
       
    obj2.save() 
    
    visitor_info = get_object_or_404(Visitor, barcode=barcode)
    visit_info = Visit.objects.filter(barcode=barcode).order_by('-date')[:10]
    return render(request, 'scanner/visitor.html', {'visit':visit_info, 
                                                    'visitor': visitor_info})
