
#	TODO: Run to find the optimal TTL
#	TODO: Run to find the optimal delay - catch error 529
#	Refreshing the page gives the same error!

#	Pre-requisites: lxml, requests
import time
import sys
import os
import requests
from lxml import html
from configs import USERNAME, PASSWORD, COURSE_NUMBERS, LOOP, REFRESH_RATE, \
    STOP_ON_SUCCESS, BEEP_ON_SUCCESS, TTL

TARGET_URL = 'https://ug3.technion.ac.il/rishum/vacancy'
LOGOUT_URL = 'https://ug3.technion.ac.il/rishum/logout'
LOGIN_URL = 'https://ug3.technion.ac.il/rishum/login'

#	Login - POST Request
session_requests = requests.session()
payload = {
    'OP': 'LI',
    'UID': USERNAME,
    'PWD': PASSWORD
}
response = session_requests.post(LOGIN_URL, payload)
response.raise_for_status()


# while True:
#	Load target page(s)
for course_number in COURSE_NUMBERS:
    course_url = TARGET_URL + '/' + course_number
    response = session_requests.get(course_url)
    response.raise_for_status()
    course_html = html.fromstring(response.content)
    vacancie = course_html.find_class('label label-success')
    vacancies = 0
    for v in vacancie:
        vacancies = vacancies + int(v.text)
    print 'Total vacancies in ' + course_number + ': ' + str(vacancies)
    if vacancies > 0:
        if BEEP_ON_SUCCESS:
            print '\a'  # cross-platform beep
        if STOP_ON_SUCCESS:
            exit(0)
if (not LOOP) or (TTL <= 0):
    # break
    pass
TTL = TTL - 1
time.sleep(float(REFRESH_RATE))
print TTL
# os.system('cls' if os.name == 'nt' else 'clear')	# cross-platform clear screen

#	Logout
response = session_requests.get(LOGOUT_URL)
response.raise_for_status()
