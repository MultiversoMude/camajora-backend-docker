# Example with the standard date and time format
from datetime import datetime, time, timedelta

strstart = '2023-02-28T14:30:00'
strend = '2023-02-28T15:30:00'

date_format = '%Y-%m-%dT%H:%M:%S'


def conv_flot_totime(t):
    hour, minute = divmod(t, 1)
    minute *= 60
    return int(hour), int(minute)


def second_between_time(start, end):
    ds = timedelta(hours=start.hour, minutes=start.minute)
    de = timedelta(hours=end.hour, minutes=end.minute)
    delta = de - ds
    return delta.total_seconds()


if __name__ == '__main__':
    credit_cost = 10
    slot = 3600
    costo_al_secondo = (credit_cost / slot)
    dt_start = datetime.strptime(strstart, date_format)
    date_end = datetime.strptime(strend, date_format)
    shour, sminute = conv_flot_totime(9)
    ehour, eminute = conv_flot_totime(19.50)
    location_start = time(shour, sminute)
    location_end = time(ehour, eminute)
    secondi_giornalieri_location = second_between_time(location_start, location_end)
    secondi_prenotazione = second_between_time(dt_start, date_end)
    number_of_days = (date_end - dt_start).days + 1
    price = 0.0
    if number_of_days > 1:
        price = number_of_days * secondi_giornalieri_location * costo_al_secondo
    else:
        price = number_of_days * secondi_prenotazione * costo_al_secondo
    print(number_of_days)
    print(price)
