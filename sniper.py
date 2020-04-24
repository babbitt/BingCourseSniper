import argparse
import sys
import datetime
import urllib.request
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from bs4 import BeautifulSoup
from random import randint
from notify_run import Notify
from pushbullet import Pushbullet

parser = argparse.ArgumentParser(description='Auto register you for a class when it becomes available.')
parser.add_argument('Season', help='["fall", "winter", "spring", "summer"]')
parser.add_argument('CRNs', type=int, nargs='+',
                   help='A CRN to be registered (int)')
parser.add_argument('PODSuser', help='Your PODS id / username (str)')
parser.add_argument('PODSpass', help='Your PODS passsword (str)')
parser.add_argument('--notify_run', help='Use Notify.run for notificaitons (just flag)', action='store_const', const=True)
parser.add_argument('--push_bullet', help='Use PushBullet for notifications - API key (str)')

args = parser.parse_args()
def notify(title,message):
	if(args.notify_run):
		args.notify_run.send(message)
	if(args.push_bullet):
		args.push_bullet.push_note(title, message)

if(args.notify_run):
	print("Notifications Via Notify.run \nUse the information below to subscribe and be notified on your device")
	args.notify_run = Notify();
	print(args.notify_run.register());
	args.notify_run.send("Welcome to course sniper. You will recieve updates about the progress of your registration via these notifications.")
if(args.push_bullet):
	print("Notifications Via PushBullet \nCheck your devices for a confirmation notification")
	args.push_bullet = Pushbullet(args.push_bullet)
	args.push_bullet.push_note("Welcome to Course Sniper!", "You will recieve updates about the progress of your registration via these notifications.")

args.Season = args.Season.lower()
if args.Season == 'spring':
    szn = 20
elif args.Season == 'summer':
    szn = 60
elif args.Season == 'fall':
    szn = 90
elif args.Season == 'winter':
    szn = 10
else:
    print('season (the first argument) should be spring, summer, winter, or fall')
    sys.exit()

year = str(datetime.datetime.now().year)
semesterNumber = year + str(szn);
while len(args.CRNs):
	register = []
	for CRN in args.CRNs:
		url = 'http://ssb.cc.binghamton.edu/banner/bwckschd.p_disp_detail_sched?term_in='+ semesterNumber + '&crn_in=' + str(CRN)
		page = urllib.request.urlopen(url)
		soup = BeautifulSoup(page, 'html.parser')
		titleTag = soup.find_all("th", class_="ddlabel")
		testTag = soup.find_all("td", class_="dddefault")
		str0 = str(titleTag[0].text)
		str1 = int(testTag[2].string)
		print("Course "+str0+" has " + str(str1) + " available seats out of " + str(testTag[1].string) + " total seats in the class")
		if(str1>0):
			register.append(True)
		else:
			register.append(False)
		
	if True in register:
		login_url = 'https://ssb.cc.binghamton.edu/banner/twbkwbis.P_GenMenu?name=bmenu.P_MainMnu&msg=WELCOME+Welcome+to+BU+BRAIN+Self+Service'
		browser = webdriver.Chrome()
		browser.get(login_url) 
		username = browser.find_element_by_name("sid")
		password = browser.find_element_by_name("PIN")
		username.send_keys(args.PODSuser)
		password.send_keys(args.PODSpass)
		browser.find_element_by_xpath("//input[@value='Login' and @type='submit']").click()
		time.sleep(1.5)
		browser.find_element_by_link_text("Student").click()
		time.sleep(1)
		browser.find_element_by_link_text("Registration").click()
		time.sleep(1)
		browser.find_element_by_link_text("Add/Drop or Withdraw from Courses").click()
		time.sleep(1)
		seasons = browser.find_elements_by_css_selector('option.value')
		for temp in seasons:
			if lower(temp.text) == lower(season + " " + year):
				temp.click()
		browser.find_element_by_xpath("//input[@value='Submit' and @type='submit']").click()
		try:
			for i in range(len(register)):
				if(register[i]):
					print("CRN "+args.CRNs[i]+" is being registered")
					crn = browser.find_element_by_id("crn_id" + str(i+1))
					crn.send_keys(args.CRNs[i])
					time.sleep(3)
			browser.find_element_by_xpath("//input[@value='Submit Changes' and @type='submit']").click()
			time.sleep(10)
			browser.quit()
			nCRNs=[]
			for i in range(len(register)):
				if(not register[i]):
					nCRNs.append(args.CRNs[i]);
				else:
					notify("Course Sniped",'CRN {CRN} has been sniped on your behalf.'.format(CRN=args.CRNs[i]))
			args.CRNs = nCRNs
		except NoSuchElementException:
			notify("CS _ ERROR","There was an error while attempting to register you. Go check it out.")
			sys.exit(NoSuchElementException)
	time.sleep(randint(30,60))
notify("All courses processed","Congrats. All courses have been registered.")
sys.exit("All classes registered for successfully")