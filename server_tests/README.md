# Server test for the parkkihubi 

## Install requirements
Python 3.1x is recommended 
`pip install python-dotenv`
`pip install requests`

## Create .env file
Create .env file from .env_example and edit the variables for the test case.

## Database and environment preparations
Add the following variables to the environment. If the item does not exists in the DB add it from the admin.
* Domain, add the name to the environment variable 'TEST_DOMAIN'
* Payment Zone, add the number to the environment variable 'TEST_PAYMENT_ZONE_NUMBER'
* Unique 'TEST_EXTERNAL_ID'
* Permit series, add the ID to the environment variable 'TEST_PERMIT_SERIES_ID'
* Two Parking areas, add the Identifiers of the areas to the environment variables 'TEST_PERMIT_AREA_IDENTIFIER_1' and 'TEST_PERMIT_AREA_IDENTIFIER_2'
Note, the entrys must be in the the same domain.


## Running test
Operator:
`python operator_api_tests.py`
Permit:
`python permit_api_tests.py`
Permit series:
`python permit_series_api_tests.py`
Enforcement:
`python enforcement_api_tests.py`
Public:

For all tests, "now news is good news", only in failures output is displayed.

