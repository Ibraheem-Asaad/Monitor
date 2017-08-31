
#	Summary:
#	Failed to make a connection due to server overload


#	Pre-requisites: lxml, requests
from lxml import html
import requests
import time
import sys
import os

# TODO: delete me
import codecs
def output_response_webpage(response, name):
	webpage_name = name + '.html'
	with codecs.open(webpage_name, 'w', response.encoding) as out:
		out.write(response.text)

def parse_argv(args, single_args_list):
	arg_flag = dict()
	
	for arg in single_args_list:
		arg_string = '-' + arg
		if arg_string in args:
			arg_flag[arg] = True
			args.remove(arg_string)
		else:
			arg_flag[arg] = False
	
	return args, arg_flag


sys.argv, arg_flag = parse_argv(sys.argv, ['loop'])

#	Configs
from credentials import username, password, course_numbers

login_url = 'https://ug3.technion.ac.il/rishum/login'
logout_url = 'https://ug3.technion.ac.il/rishum/logout'
target_url = 'https://ug3.technion.ac.il/rishum/vacancy'

#	Login - POST Request
session_requests = requests.session()
payload = {
	'OP': 'LI',
	'UID': username, 
	'PWD': password
}
response = session_requests.post(login_url, payload)
response.raise_for_status()

loop = True

while loop:
	#	Load target page(s)
	for course_number in course_numbers:
		
		course_url = target_url + '/' + course_number
		response = session_requests.get(course_url)
		output_response_webpage(response,'target')
		response.raise_for_status()
		
		html_target = html.fromstring(response.content)
		vacancie = html_target.find_class('label label-success')
		
		vacancies = 0
		for v in vacancie:
			vacancies = vacancies + int(v.text)
		print('Total vacancies in ' + course_number + ': ' + str(vacancies))
		if vacancies > 0:
			print '\a' # Beep
		loop = arg_flag['loop']
	
	time.sleep(5)
	os.system('cls' if os.name == 'nt' else 'clear')

#	Logout
response = session_requests.post(logout_url, payload)
response.raise_for_status()
