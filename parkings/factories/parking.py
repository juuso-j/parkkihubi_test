from datetime import timedelta

import factory
import pytz
from django.contrib.gis.geos import Point

from parkings.factories import EnforcementDomainFactory
from parkings.models import Parking, PaymentZone

from .faker import fake
from .operator import OperatorFactory

CAPITAL_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ'


def generate_registration_number():
    letters = ''.join(fake.random.choice(CAPITAL_LETTERS) for _ in range(3))
    numbers = ''.join(fake.random.choice('0123456789') for _ in range(3))
    return '%s-%s' % (letters, numbers)


def create_payment_zone(**kwargs):
    from parkings.tests.api.enforcement.test_check_parking import create_area_geom
    kwargs.setdefault('domain', EnforcementDomainFactory())
    kwargs.setdefault('number', 1)
    kwargs.setdefault('code', "1")
    kwargs.setdefault('name', "Maksuvyöhyke 1")
    kwargs.setdefault('geom', create_area_geom())
    zone = PaymentZone.objects.create(**kwargs)
    return zone


class ParkingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parking

    location = factory.LazyFunction(
        lambda: Point(24.915 + fake.random.uniform(0, 0.040), 60.154 + fake.random.uniform(0, 0.022))
    )
    operator = factory.SubFactory(OperatorFactory)
    registration_number = factory.LazyFunction(generate_registration_number)
    time_start = factory.LazyFunction(lambda: fake.date_time_between(start_date='-2h', end_date='-1h', tzinfo=pytz.utc))
    time_end = factory.LazyFunction(lambda: fake.date_time_between(start_date='+1h', end_date='+2h', tzinfo=pytz.utc))
    zone = factory.LazyFunction(create_payment_zone)


class DiscParkingFactory(ParkingFactory):
    is_disc_parking = True


def get_time_far_enough_in_past():
    return fake.date_time_this_decade(before_now=True, tzinfo=pytz.utc) - timedelta(days=7, seconds=1)


class HistoryParkingFactory(ParkingFactory):
    time_end = factory.LazyFunction(get_time_far_enough_in_past)
    time_start = factory.lazy_attribute(
        lambda o:
        o.time_end - timedelta(seconds=fake.random.randint(0, 60*24*14))
        if o.time_end is not None
        else get_time_far_enough_in_past()
    )
