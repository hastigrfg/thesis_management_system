from datetime import datetime, timedelta

def get_current_date():
    return datetime.now()

def format_date(date_obj, format_str="%Y-%m-%d %H:%M:%S"):
    return date_obj.strftime(format_str)

def parse_date(date_str, format_str="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(date_str, format_str)

def months_diff(date1, date2):
    return (date2.year - date1.year) * 12 + (date2.month - date1.month)
