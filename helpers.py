import datetime

from constants import DATE_FORMAT


def str_to_date(d_str):
    return datetime.datetime.strptime(d_str, DATE_FORMAT).date()


def date_to_str(date):
    return date.strftime(DATE_FORMAT)
