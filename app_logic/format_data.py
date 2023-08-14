def format_data(data, current_week):
    formated_data = {}
    # Format the data in a usable way
    for elem in data:
        formated_data[elem['username']] = {}
        reports = elem.get('reports')
        if reports:
            current_week_reports = reports.get(current_week)
            if current_week_reports:
                formated_data[elem['username']]['monday'] = current_week_reports.get('monday')
                formated_data[elem['username']]['tuesday'] = current_week_reports.get('tuesday')
                formated_data[elem['username']]['wednesday'] = current_week_reports.get('wednesday')
                formated_data[elem['username']]['thursday'] = current_week_reports.get('thursday')
                formated_data[elem['username']]['friday'] = current_week_reports.get('friday')
                formated_data[elem['username']]['saturday'] = current_week_reports.get('saturday')
                formated_data[elem['username']]['sunday'] = current_week_reports.get('sunday')

    return formated_data