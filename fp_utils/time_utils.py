from datetime import datetime as dt
from pytz import timezone
from dateutil.relativedelta import relativedelta


def get_now_time():
    KST = dt.now(timezone('Asia/Seoul'))
    return KST


def generate_date_strings(start_date: dt, end_date: dt, date_format: str = '%Y%m'):
    date_strings = []
    current_date = start_date
    
    while current_date <= end_date:
        date_strings.append(current_date.strftime(date_format))
        current_date += relativedelta(months=1)
    
    return date_strings