def format_data(data, current_week):
    formated_data = {}
    # Format the data in a usable way
    for elem in data:
        formated_data[elem['username']] = {}
        formated_data[elem['username']]['monday'] = elem['reports'][current_week].get('monday')
        formated_data[elem['username']]['tuesday'] = elem['reports'][current_week].get('tuesday')
        formated_data[elem['username']]['wednesday'] = elem['reports'][current_week].get('wednesday')
        formated_data[elem['username']]['thursday'] = elem['reports'][current_week].get('thursday')
        formated_data[elem['username']]['friday'] = elem['reports'][current_week].get('friday')
        formated_data[elem['username']]['saturday'] = elem['reports'][current_week].get('saturday')
        formated_data[elem['username']]['sunday'] = elem['reports'][current_week].get('sunday')
		
    return formated_data