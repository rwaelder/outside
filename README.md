# outside
Python weather app



Requires Map Quest API key. Key can be obtained by creating an account at [developer.mapquest.com](https://developer.mapquest.com)

Add key to 'outside.conf' file

<b>How to use</b>

Command line usage. 
Optionally argument based.

No command line arguments and it will prompt for city and state.
Assumes state in two-letter abbreviation.
Spaces in city name are fine if there is also a space before the state code.

City and state can be argument passed in the following manner:

python outside.py city,state

python outside.py city state
