
"""Credentials and configurations for monitor module"""


USERNAME = ''
PASSWORD = ''
COURSE_NUMBERS = {'234118'}  # {324580}
REFRESH_RATE = 5  # seconds {5}
STOP_ON_SUCCESS = False  # {True}
BEEP_ON_SUCCESS = False  # {True}
TTL = 45  # Time to live (repititions) {255}
#	TODO: Run to find the optimal TTL
# MAX_TLL: 45 on a 5 REFRESH_RATE
#	TODO: Run to find the optimal delay - catch error 529
#	Refreshing the page gives the same error!
