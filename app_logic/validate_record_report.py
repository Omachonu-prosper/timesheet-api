def validate_record_report(json):
	response = {}
	date = json.get('date')
	project = json.get('project')
	task = json.get('task')
	status = json.get('status')
	link = json.get('link')
	duration = json.get('duration')

	if not date or not project or not task or not status or not link or not duration:
		response['message'] = 'Missing required parameter'
		response['error'] = True
		response['error-code'] = 400
		return response
	
	response['date'] = date
	response['project'] = project
	response['task'] = task
	response['status'] = status
	response['link'] = link
	response['duration'] = duration
	return response