import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transport_services_server.settings')

import django
django.setup()

import datetime
from main.models import DataAnalyst, Journey
from django.contrib.auth.models import User
from django.core.files import File

def populate():

    #need unique identifier for journeys


    journeys = [
        {
            'start_date' : datetime.date(2020, 8, 11),
            'end_date' : datetime.date(2020, 8, 11),
            'driver' : "Chris",
            'start_location' : "Vet School",
            'destinations1' : "Somewhere",
            'destinations2' : None,
            'destinations3' : None,
            'purpose' : "Supplies",
            'plate_number' : "AB70DHD",
            'no_of_pass' : "2",
            'start_time' : datetime.time(hour=1, minute=1),
            'end_time' : datetime.time(hour=2, minute=10),
            'mileage_start': 12000,
            'mileage_finish' : 12004,
            'approved' : True,
            'round_trip' : True
        },
        {           
            'start_date' : datetime.date(2021, 2, 10),
            'end_date' : datetime.date(2021, 2, 11),
            'driver' : "Joe",
            'start_location' : "Uni",
            'destinations1' : "Shops",
            'destinations2' : "City centre",
            'destinations3' : None,
            'purpose' : "Travel People",
            'plate_number' : "AB70DHD",
            'no_of_pass' : "0",
            'start_time' : datetime.time(hour=10, minute=15),
            'end_time' : datetime.time(hour=11, minute=00),
            'mileage_start': 12004,
            'mileage_finish' : 12010,
            'approved' : False,
            'round_trip' : True
        },
        {           
            'start_date' : datetime.date(2019, 12, 12),
            'end_date' : datetime.date(2019, 12, 12),
            'driver' : "Danny",
            'start_location' : "Vet School",
            'destinations1' : "Somewhere",
            'destinations2' : "Here",
            'destinations3' : "There",
            'purpose' : "Supplies",
            'plate_number' : "AB70DHD",
            'no_of_pass' : "1",
            'start_time' : datetime.time(hour=20, minute=0),
            'end_time' : datetime.time(hour=21, minute=0),
            'mileage_start': 16010,
            'mileage_finish' : 16042,
            'approved' : True,
            'round_trip' : False
        },
        {           
            'start_date' : datetime.date(2022, 1, 24),
            'end_date' : datetime.date(2022, 1, 25),
            'driver' : "Jason",
            'start_location' : "Tesco",
            'destinations1' : "Shops",
            'destinations2' : None,
            'destinations3' : None,
            'purpose' : "Supplies",
            'plate_number' : "AB70DHD",
            'no_of_pass' : "4",
            'start_time' : datetime.time(hour=12, minute=00),
            'end_time' : datetime.time(hour=12, minute=45),
            'mileage_start': 100400,
            'mileage_finish' : 100402,
            'approved' : False,
            'round_trip' : False
        },
        {           
            'start_date' : datetime.date(2022, 1, 23),
            'end_date' : datetime.date(2022, 1, 24),
            'driver' : "Bobby",
            'start_location' : "Vet School",
            'destinations1' : "Somewhere",
            'destinations2' : None,
            'destinations3' : None,
            'purpose' : "Supplies",
            'plate_number' : "AB70DHD",
            'no_of_pass' : "4",
            'start_time' : datetime.time(hour=12, minute=00),
            'end_time' : datetime.time(hour=12, minute=45),
            'mileage_start': 100400,
            'mileage_finish' : 100402,
            'approved' : False,
            'round_trip' : False
        },
        {           
            'start_date' : datetime.date(2022, 1, 23),
            'end_date' : datetime.date(2022, 1, 25),
            'driver' : "Orange",
            'start_location' : "Vet School",
            'destinations1' : "Somewhere",
            'destinations2' : None,
            'destinations3' : None,
            'purpose' : "Supplies",
            'plate_number' : "AB70DHD",
            'no_of_pass' : "4",
            'start_time' : datetime.time(hour=12, minute=00),
            'end_time' : datetime.time(hour=12, minute=45),
            'mileage_start': 100400,
            'mileage_finish' : 100402,
            'approved' : False,
            'round_trip' : False
        }
    ]
    """
    data_analysts = [
        {
            'name' : "John Smith",
            'username' : "JohnSmith4"
        },
        {
            'name' : "Barry Pete",
            'username' : "BigBarry"
        },
        {
            'name' : "Mohammed",
            'username' : "CoolMan123"
        }
    ]
    """
    if not User.objects.filter(username='Viola').exists():
        user=User.objects.create_user('Viola', password='JohnCena420')
        user.is_superuser=True
        user.is_staff=True
        user.save()

    if not User.objects.filter(username='Grantt').exists():
        user=User.objects.create_user('Grantt', password='Grantt')
        user.is_superuser=True
        user.is_staff=True
        user.save()


    #for p in data_analysts:
     #   add_analyst(p["username"], p["name"])

    for p in journeys:
        add_journey(p["driver"], p["start_date"], p["end_date"], p["start_location"], p["destinations1"], p["destinations2"], p["destinations3"], p["purpose"], p["plate_number"], p["no_of_pass"], p["start_time"], p["end_time"], p["mileage_start"], p["mileage_finish"],p["approved"],p["round_trip"])

def add_analyst(username, name):
    analyst = DataAnalyst.objects.get_or_create(username=username, name=name)[0]
    analyst.save()
    return analyst

def add_journey(driver, start_date, end_date, start_location, destinations1, destinations2, destinations3, purpose, plate_number, no_of_pass, start_time, end_time, mileage_start, mileage_finish, approved, round_trip):
    journey = Journey.objects.get_or_create(driver=driver, start_date=start_date, end_date=end_date, start_location=start_location, destinations1=destinations1, destinations2=destinations2, destinations3=destinations3, purpose=purpose, plate_number=plate_number, no_of_pass=no_of_pass, start_time=start_time, end_time=end_time, mileage_start=mileage_start, mileage_finish=mileage_finish, approved=approved, round_trip=round_trip)[0]
    journey.save()
    return journey


if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Finished populating")
