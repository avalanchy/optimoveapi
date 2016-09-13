import datetime

from .constants import DATE_FORMAT


def str_to_date(d_str):
    """Converts optimove-date-string to python-date object"""
    return datetime.datetime.strptime(d_str, DATE_FORMAT).date()


def date_to_str(date):
    """Converts python-date object to optimove-date-string """
    return date.strftime(DATE_FORMAT)
