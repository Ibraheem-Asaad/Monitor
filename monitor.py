
"""Monitor university's course registeration website for vacancies"""


import time
import sys
import os
import requests
from lxml import html
from configs import USERNAME, PASSWORD, COURSE_NUMBERS, REFRESH_RATE, \
    STOP_ON_SUCCESS, BEEP_ON_SUCCESS, TTL

TARGET_URL = 'https://ug3.technion.ac.il/rishum/vacancy'
LOGOUT_URL = 'https://ug3.technion.ac.il/rishum/logout'
LOGIN_URL = 'https://ug3.technion.ac.il/rishum/login'


def login(session):
    """Login to the university's course registeration website"""
    response = session.get(LOGIN_URL)
    response.raise_for_status()
    login_form = html.fromstring(response.content).forms[0]
    payload = dict(login_form.fields)
    payload['UID'] = USERNAME
    payload['PWD'] = PASSWORD
    response = session.post(LOGIN_URL, payload)


def query(session, course_number):
    """Query and display total number of vacancies for a specific course"""
    course_url = TARGET_URL + '/' + course_number
    response = session.get(course_url)
    response.raise_for_status()
    course_html = html.fromstring(response.content)
    vacancie_list = course_html.find_class('label label-success')
    vacancies = 0
    for vacancy in vacancie_list:
        vacancies = vacancies + int(vacancy.text)
    print 'Total vacancies in ' + course_number + ': ' + str(vacancies)
    if vacancies > 0:
        if BEEP_ON_SUCCESS:
            print '\a'  # cross-platform beep
        if STOP_ON_SUCCESS:
            exit(0)


def logout(session):
    """Logout from the university's course registeration website"""
    response = session.get(LOGOUT_URL)
    response.raise_for_status()


if __name__ == '__main__':
    SESSION = requests.session()
    login(SESSION)
    for rep in range(0, TTL):
        for course_number in COURSE_NUMBERS:
            query(SESSION, course_number)
            print rep
            time.sleep(float(REFRESH_RATE))
            # cross-platform clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
    logout(SESSION)
