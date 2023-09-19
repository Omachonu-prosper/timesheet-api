# Test Module for Timesheet-API

## Environment
The tests are written to be tested on the local developmnet environments

## Requirements
* Flask server - running on localhost:5000 (127.0.0.1:5000)
* Mongodb server - running on (mongodb://localhost:27017)
* An admin user created with `username` and `password` in the admins collection in mongodb
* Environment variables
```
ADMIN_PASSWORD=<admin_password> # If not present tests on the admin login endpoint would fail
ADMIN_USERNAME=<admin_username> # If not present tests on the admin login endpoint would fail
```


Once the requirements have been met run `python -m unittest discover tests`