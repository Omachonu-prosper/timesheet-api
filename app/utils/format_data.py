def format_data(data, current_week):
    formated_data = []

    # Format the data in a usable way
    for elem in data:
        current_user = {}

        # Add the users details to their reports
        current_user['user'] = {
            'username': elem['username'],
            'email': elem['email'],
            'id': str(elem['_id'])
        }

        # The reports for current_week
        current_user['report'] = {}
        
        reports = elem.get('reports')
        if reports:
            current_week_reports = reports.get(current_week)
            if current_week_reports:
                current_user['report']['monday'] = current_week_reports.get('monday')
                current_user['report']['tuesday'] = current_week_reports.get('tuesday')
                current_user['report']['wednesday'] = current_week_reports.get('wednesday')
                current_user['report']['thursday'] = current_week_reports.get('thursday')
                current_user['report']['friday'] = current_week_reports.get('friday')
                current_user['report']['saturday'] = current_week_reports.get('saturday')
                current_user['report']['sunday'] = current_week_reports.get('sunday')
        
        formated_data.append(current_user)

    return formated_data