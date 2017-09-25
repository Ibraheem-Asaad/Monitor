
#	TODO: Run to find the optimal TTL
#	TODO: Run to find the optimal delay - catch error 529
#	Refreshing the page gives the same error!

#	Pre-requisites: lxml, requests
from lxml import html
import requests
import time
import sys
import os
#	Configs: username, password, course_numbers, loop, refresh_rate, stop_on_success, beep_on_success, ttl
from configs import *


target_url = 'https://ug3.technion.ac.il/rishum/vacancy'
logout_url = 'https://ug3.technion.ac.il/rishum/logout'
login_url = 'https://ug3.technion.ac.il/rishum/login'

#	Login - POST Request
session_requests = requests.session()
payload = {
	'OP': 'LI',
	'UID': username, 
	'PWD': password
}
response = session_requests.post(login_url, payload)
response.raise_for_status()


while True:
	#	Load target page(s)
	for course_number in course_numbers:
		
		course_url = target_url + '/' + course_number
		response = session_requests.get(course_url)
		response.raise_for_status()
		
		course_html = html.fromstring(response.content)
		vacancie = course_html.find_class('label label-success')
		
		vacancies = 0
		for v in vacancie:
			vacancies = vacancies + int(v.text)
		print('Total vacancies in ' + course_number + ': ' + str(vacancies))
		if vacancies > 0:
			if beep_on_success:
				print '\a'	# cross-platform beep
			if stop_on_success:
				exit(0)
		
	if (not loop) or (ttl <= 0):
		break
		
	ttl = ttl - 1
	time.sleep(float(refresh_rate))
	print(ttl)
	#os.system('cls' if os.name == 'nt' else 'clear')	# cross-platform clear screen

#	Logout
response = session_requests.get(logout_url)
response.raise_for_status()
