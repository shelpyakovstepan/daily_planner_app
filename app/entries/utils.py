from datetime import datetime

import pytz


def check_availability_by_date_end(date_end):
    """
    Вовзращает True, если дата окончания МЕНЬШЕ или РАВНА сегодняшней дате,
    тоесть дата окончания была ДО сегодняшней даты.
    """
    if datetime.strptime(str(date_end), "%Y-%m-%d").date() <= datetime.now(pytz.timezone("Europe/Moscow")).date():
        return True
    return False

def check_availability_by_date_start_before_date_now(date_start):
    """
    Возвращает True, если дата начала МЕНЬШЕ или РАВНА сегодняшней дате,
    тоесть дата начала была ДО сегодняшней даты.
    """
    if datetime.strptime(str(date_start), "%Y-%m-%d").date() <= datetime.now(pytz.timezone("Europe/Moscow")).date():
        return True
    return False

def check_availability_by_date_start_after_date_now(date_start):
    """
    Возвращает True, если дата начала БОЛЬШЕ сегодняшней даты,
    тоесть дата начала будет ПОСЛЕ сегодняшней даты.
    """
    if datetime.strptime(str(date_start), "%Y-%m-%d").date() > datetime.now(pytz.timezone("Europe/Moscow")).date():
        return True
    return False

def check_delta_days(date_start, date_end):
    """Возвращает True, если день окончания ДО дня начала."""
    delta = date_end - date_start
    if delta.days <= 0:
        return True
    return False