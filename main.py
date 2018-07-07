import requests, sys, json
from captcha import getCaptchaText

URLS = [
	'https://erp.iitkgp.ac.in/StudentPerformanceV2/auth/login.htm',
	'https://erp.iitkgp.ac.in/StudentPerformanceV2/auth/getCaptchaCode.htm',
	'https://erp.iitkgp.ac.in/StudentPerformanceV2/auth/PassImageServlet/{}',
	'https://erp.iitkgp.ac.in/StudentPerformanceV2/auth/authenticate.htm',
	'https://erp.iitkgp.ac.in/StudentPerformanceV2/secure/StudentPerfDtls.htm?rollno={}'
]
CAPTCHA_IMG = 'captcha.jpeg'
JSON_CONTENT = 'json/application;charset=ISO-8859-1'

def checkStatus(code):
	if code not in [200, 302]:
		sys.exit('Error: ' + str(code))

def main(roll, dob):
	r0 = requests.get(URLS[0])
	checkStatus(r0.status_code)

	headers = {'Cookie' : r0.headers['Set-Cookie']}
	r1 = requests.get(URLS[1], headers=headers)
	checkStatus(r1.status_code)

	r2 = requests.get(URLS[2].format(r1.text), stream=True)
	checkStatus(r2.status_code)
	with open(CAPTCHA_IMG,'wb') as file:
		for chunk in r2:
			file.write(chunk)

	data = {
		'rollno' : roll,
		'dob' : dob,
		'passline' : getCaptchaText(CAPTCHA_IMG)
	}
	r3 = requests.post(URLS[3], data=data, headers=headers)
	checkStatus(r3.status_code)

	r4 = requests.get(URLS[4].format(roll), headers=headers)
	checkStatus(r4.status_code)
	if r4.headers['Content-Type'] == JSON_CONTENT:
		return r4.text
	else:
		return False


if __name__ == '__main__':
	roll = input("Roll Number: ")
	dob = input("Date of Birth (dd-mm-yyyy): ")
	data = main(roll, dob)
	if data:
		json_data = json.loads(data)
		for sem in json_data:
			print('Semester ' + sem['semno'] + ': ' + sem['nccgsg'])
	else:
		print('Data mismatch!')
