import json

from django.core import serializers
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .form import *
from .models import Journey
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
import datetime
from django.db.models import Count
import csv
from django.contrib import messages

import matplotlib.pyplot as plt
import urllib
import base64
import io
import numpy as np


# Create your views here.
def index(request):
    return render(request, "main/index.html")


def analytics(request):

    current_date = datetime.date.today()
    week_ago_date = current_date - datetime.timedelta(days=7)
    cur_date = current_date.strftime("%b %d")
    week_ago = week_ago_date.strftime("%b %d")
    weeks_journeys = Journey.objects.filter(start_date__range=[week_ago_date, current_date], approved=True)

    average_miles = 0
    for journey in weeks_journeys:
        journey.miles()
        average_miles += journey.total_miles
    if (weeks_journeys.count() > 0):
        average_miles = round(average_miles / weeks_journeys.count())


    #Graph for frequency
    x_freq = []
    y_freq = []
    x_purp = []
    y_purp = []
    x_dest = []
    y_dest = []
    for i in range(7):
        date = week_ago_date + datetime.timedelta(days=i+1)
        current_date = date
        x_freq.append(current_date.strftime("%b %d"))
        y_freq.append(weeks_journeys.filter(start_date=date).count())

    a = Journey.objects.values_list('purpose').annotate(journey_count=Count('purpose')).order_by('-journey_count')
    if a.count() > 0:
        counter = 0
        other = 0
        for j in a:
            if counter < 3:
                counter+=1;
                x_purp.append(j[0])
                y_purp.append(j[1])
            else:
                other += j[1]
        x_purp.append("Other")
        y_purp.append(other)

    
    #Graph for frequency
    plt.subplot(3,1,1)
    plt.bar(x_freq,y_freq, color='lightgreen')
    plt.ylabel('Journeys')

    fig = plt.gcf()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    freq = urllib.parse.quote(string)


    #Graph for purpose
    plt.subplot(3,1,2)
    plt.ylabel('Purposes')
    plt.bar(x_purp,y_purp, color='lightblue')
    plt.xticks(x_purp)

    fig = plt.gcf()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    dests = urllib.parse.quote(string)
    plt.subplots_adjust()

    #Destinations
    plt.subplot(3,1,3)
    plt.ylabel('Destinations')
    [float(i) for i in y_purp]
    plt.pie(y_purp)

    fig = plt.gcf()

    buf = io.BytesIO()
    fig.subplots_adjust(hspace=.5)
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    dests = urllib.parse.quote(string)



    context_dict = {}
    context_dict['average_miles'] = average_miles
    context_dict['graphs'] = dests

    return render(request,"main/analytics/analytics.html", context=context_dict)


def report_journey(request):
    return render(request, "main/journey/report-journey.html")

def journey_details(request):

    form = JourneyForm()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # check whether it's valid:
        form = JourneyForm(data=request.POST)
        print(form.errors)
        context_dict={}
        if form.is_valid():
            # process the data in form.cleaned_data as required
            cleaned_form = form.cleaned_data

            if cleaned_form['end_date'] < cleaned_form['start_date']:
                return HttpResponse('Error - End date is before start date!')
            elif (cleaned_form['end_date'] == cleaned_form['start_date']) and (cleaned_form['end_time'] < cleaned_form['start_time']):
                context_dict['messages'] = messages
                return HttpResponse('Error - End time is before start time!')
            else:
                journey = Journey.objects.get_or_create(driver=cleaned_form['driver'], start_date=cleaned_form['start_date'],
                end_date=cleaned_form['end_date'],
                purpose=cleaned_form['purpose'], plate_number=cleaned_form['plate_number'],
                start_location=cleaned_form['start_location'], destinations1=cleaned_form['destinations1'],
                destinations2=cleaned_form['destinations2'], destinations3=cleaned_form['destinations3'],
                no_of_pass=cleaned_form['no_of_pass'],start_time=cleaned_form['start_time'],
                end_time=cleaned_form['end_time'], mileage_start=cleaned_form['mileage_start'],
                mileage_finish=cleaned_form['mileage_finish'], round_trip=cleaned_form['is_round_trip'])[0]
                journey.save()
                # redirect to a new URL:
                return HttpResponse('Successfully reported your journey!')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = JourneyForm()

    return render(request,"main/journey/journey-details.html", {'form': form})

def dashboard(request):
    pending = Journey.objects.filter(approved=False).count()
    current_date = datetime.date.today()
    week_ago_date = current_date - datetime.timedelta(days=7)
    cur_date = current_date.strftime("%b %d")
    week_ago = week_ago_date.strftime("%b %d")
    weeks_journeys = Journey.objects.filter(start_date__range=[week_ago_date, current_date], approved=True)
    reported_journeys = weeks_journeys.count()
    average_miles=0
    common_purpose = None
    for journey in weeks_journeys:
        journey.miles()
        average_miles += journey.total_miles
    if (reported_journeys > 0):
        average_miles = round(average_miles / reported_journeys)
        common_purpose = Journey.objects.values_list('purpose').annotate(journey_count=Count('purpose')).order_by('-journey_count')[0][0]

    context_dict = {}
    context_dict['pending'] = pending
    context_dict['cur_date'] = cur_date
    context_dict['week_ago'] = week_ago
    context_dict['reported_journeys'] = reported_journeys
    context_dict['average_miles'] = average_miles
    context_dict['common_purpose'] = common_purpose
    return render(request,"main/analytics/dashboard.html", context=context_dict)

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                #Signs the user in with the details supllied once they create an account
                auth_login(request, user)
                return redirect(reverse("main:dashboard"))
            else:
                return HttpResponse("Your account has been disabled.")

        else:
            return HttpResponse("Incorrect username or password.")

    else:
        return render(request, 'main/admin/admin-login.html')

def analysis(request):
    return render(request,"main/analytics/analysis.html")


#def account_manager(request):
#    return render(request,"main/analytics/account-manager.html")

def data_table(request):
    order_by = request.GET.get('order_by', '-start_date')
    journeys = Journey.objects.filter(approved=True).order_by(order_by)
    context_dict = {}
    context_dict['journeys'] = journeys
    return render(request,"main/analytics/data-table.html", context=context_dict)

def export_data(request):
    return render(request,"main/analytics/export-data.html")

def export_data_file(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="TransportServices.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Start Date', 'End Date', 'Driver', 'Plate Number', 'Start Location', 'First Destination', 'Second Destination',
        'Third Destination', 'Purpose', 'Number of Passengers', 'Start Time', 'End Time', 'Starting Mileage', 'Ending Mileage', 'Round Trip?'])

    journeys = Journey.objects.filter(approved=True)
    for journey in journeys:
        writer.writerow([journey.start_date, journey.end_date, journey.driver, journey.plate_number, journey.start_location,
            journey.destinations1, journey.destinations2, journey.destinations3, journey.purpose, journey.no_of_pass,
            journey.start_time, journey.end_time, journey.mileage_start, journey.mileage_finish, journey.round_trip])

    return response

def pending_data(request):
    order_by = request.GET.get('order_by', 'start_date')
    journeys = Journey.objects.filter(approved=False).order_by(order_by)
    for journey in journeys:
        journey.update_vehicle_type()
        journey.miles()
        journey.save()
    context_dict = {}
    context_dict['journeys'] = journeys
    return render(request,"main/analytics/pending-data.html", context=context_dict)

def approve_journey(request):
    data = {'success': False}
    if request.method=='POST':
        id = request.POST.get('id')
        journey = Journey.objects.get(id=id)
        journey.approved = True
        journey.save()
        data = {'success': True}

    return JsonResponse(data)

def reject_journey(request):
    data = {'success': False}
    if request.method=='POST':
        id = request.POST.get('id')
        Journey.objects.filter(id=id).delete()
        data = {'success': True}

    return JsonResponse(data)


@login_required
def logout(request):
    auth_logout(request)
    return render(request,"main/admin/admin-login.html")
