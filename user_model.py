"""Models user data
"""

users = [
	{
		"id": 1,
		"username": "Johndoe1",
		"first-name": "John",
		"last-name": "Doe",
		"middle-name": "Don",
		"password": "password",
		"email": "johndoe@example.com",
		"created-at": "2023-07-30 18:34:41.846230",
		"role": "supervisee",
		"reports": [
			{
				"id": 1,
				"date": "2023-07-11",
				"project": "Revenue tracking API",
				"task": "Refactored API",
				"status": "Completed",
				"link": "https://google.com",
				"duration": "1 hour",
				"week-start": "2023-07-10",
				"day-of-week": "Tuesday",
				"created-at": "2023-07-30 18:50:41.846230"
			}
		]
	}
]