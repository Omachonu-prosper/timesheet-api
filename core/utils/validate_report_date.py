from datetime import datetime, timedelta
from .get_day_of_week import get_day_of_week

def validate_report_date(date):
    response = {}
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except:
        response['message'] = 'Date is not a valid datetime format'
        response['error-code'] = 400
        response['error'] = True
        return response
    
    # Get the start of the week from the provided date
    week_start = date - timedelta(days=date.weekday())
    created_at = datetime.now()
    # Get the day of the week from the provided date
    day_of_week = get_day_of_week(date)
    
    now = datetime.now()
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    current_week = today - timedelta(days=today.weekday())

    # The report to be recorded is that of a previous week
    if current_week != week_start:
        # Once it is past 8:00am on Monday do not accept submissions for any other week apart from the current week
        # today.weekday == 0 (shows that it is a monday)
        # now.hour < 8 (the time is not yet 8:00am)
        # week_start == current_week - timedelta(weeks=1) 
        # 	(shows that the report we are trying to submit is a report of the past week
        # 	and so can be allowed since the time is not yet 8:00am)
        if today.weekday() == 0 and now.hour < 8 and week_start == current_week - timedelta(weeks=1):
            pass
        else:
            response['message'] = "Failed to record report: submission window exceeded"
            response['error-code'] = 403
            response['error'] = True
            return response
        
    response['date'] = date
    response['created-at'] = created_at
    response['day'] = day_of_week
    response['week'] = week_start.strftime('%Y-%m-%d')
    return response