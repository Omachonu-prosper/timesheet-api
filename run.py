import os
from app import create_app

app = create_app()
if __name__ == '__main__':
	app_environment = os.environ.get('APP_ENVIRONMENT', 'development')
	if app_environment.lower() == 'production':
		app.run()
	else:
		app.run(debug=True)