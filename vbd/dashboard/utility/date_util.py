import datetime
import time

def get_current_day_start_date(d_time=datetime.datetime.utcnow(), t_format="%Y-%m-%d %H:%M:%S"):
    time_string = '%s-%s-%s 00:00:00' % (d_time.year, d_time.month, d_time.day)
    dt = datetime.datetime.strptime(time_string, t_format)
    return dt

def get_datetime_after(t_date=datetime.datetime.utcnow(), delta_seconds=0, delta_minutes=0, delta_hours=0, delta_days=0, delta_milliseconds=0):
    return t_date + datetime.timedelta(seconds=delta_seconds, minutes=delta_minutes, hours=delta_hours, days=delta_days, milliseconds=delta_milliseconds)

def get_datetime_before(t_date=datetime.datetime.utcnow(), delta_seconds=0, delta_minutes=0, delta_hours=0, delta_days=0, delta_milliseconds=0):
    return t_date - datetime.timedelta(seconds=delta_seconds, minutes=delta_minutes, hours=delta_hours, days=delta_days, milliseconds=delta_milliseconds)

def datetime_2_long(t_datetime):
    if type(t_datetime) is not datetime.datetime:
        print 'Warn, parameter t_datetime is not a datetime.datetime, please check'
        return 0
    
    t_format = "%Y-%m-%d %H:%M:%S"
    strtime = t_datetime.strftime(t_format)
    t_tuple = time.strptime(strtime, t_format)
    return time.mktime(t_tuple)

def convert_long_2_gmt_time(time_long):
    t_tuple = time.localtime(time_long)
    dt = datetime.datetime(*t_tuple[:6])
    
    GMT_FORMAT = '%a %b %d %Y %H:%M:%S GMT+0800 (CST)'
    return dt.strftime(GMT_FORMAT)

if __name__ == '__main__':
    print convert_long_2_gmt_time(1500283285.268)
    print convert_long_2_gmt_time(1500278096.591)