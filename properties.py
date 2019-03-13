# Non-MacOS users can change it to Chrome/Firefox.
BROWSER = "Chrome" # can be Chrome/Safari/Firefox
MATCH_URL = "http://www.espncricinfo.com/series/19059/commentary/1168246/india-vs-australia-5th-odi-aus-in-ind-2018-19"

# Match start timings according to where the script is being run.
MATCH_START_HOURS = 13
MATCH_START_MINUTES = 30
MATCH_END_HOURS = 23
MATCH_END_MINUTES = 0
LOG_FILENAME = 'script_logs.log'

# This tells whether the script is running in test mode or not. If yes, the actual data sent is less, for better debugging.
IS_TEST_MODE = False
