import calendar
import datetime
import logging

import pytz

timezone = pytz.timezone('Europe/Rome')


def extract_year_month_day(param):
    a, b, c = param.split('-', 2)
    return int(a), int(b), int(c)


def extract_time_interval(param):
    a, b = param.split('-', 1)
    return int(a), int(b)


def build_range(year, month, day, start, end):
    target_start = datetime.datetime(year, month, day, start, 0)
    target_end = datetime.datetime(year, month, day, end, 59)
    utc_target_start = timezone.localize(target_start).astimezone(pytz.utc).replace(tzinfo=None)
    utc_target_end = timezone.localize(target_end).astimezone(pytz.utc).replace(tzinfo=None)
    return utc_target_start, utc_target_end


if __name__ == '__main__':
    year, month, day = extract_year_month_day('2023-01-01')
    start, end = extract_time_interval('01-23')
    print('{}-{:02}-{:02}'.format(year, month, day))
    utc_target_start, utc_target_end = build_range(year, month, day, start, end)
    print(utc_target_start)
    print(utc_target_end)
