from HTMLParser import HTMLParser
import getpass, os, requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

homepageURL = 'https://lms.iiitb.ac.in/moodle/my/'
loginURL = 'https://lms.iiitb.ac.in/moodle/login/index.php'

class Login:
	def __init__(self):
		self.getLoginCredentials()

	def getLoginCredentials(self):
		username = raw_input("Username: ")
		password = getpass.getpass()

		self.credentials = {'username': username,
		                    'password': password}

	def getCredentials(self):
		return self.credentials

class RetrieveHTML:
	def login(self, data):
		global loginURL
		self.c = requests.session()
		self.c.post(loginURL, data.getCredentials(), verify = False)

	def retrieveHTML(self):
		resp = self.c.get(homepageURL)
		self.html = resp.text

	def getHTML(self):
		return self.html

class Student:
	def setImgURL(self, imgURL):
		'''Although Image URL is not used in this program it is stored for future GUI implementation'''
		self.imgURL = imgURL

	def setName(self, name):
		self.name = name

	def setTime(self, time):
		self.time = time

	def setRollno(self, rollno):
		self.rollno = rollno

	def __str__(self):
		return "Name: " + self.name + "\n" + "Rollnumber: " + self.rollno + "\n" + "Active for: " + self.time + "\n"

class StudentList:
	def __init__(self):
		self.stulist = list()

	def stuAdd(self, student):
		self.stulist.append(student)

	def printData(self):
		for student in self.stulist:
			print student

class LMSDataScraper(HTMLParser):
	def __init__(self, students):
		HTMLParser.__init__(self)
		self.start = False
		self.students = students

	def handle_starttag(self, tag, attrs):
		if tag == "div":
			for attr in attrs:
				if attr[1] == "user":
					self.start = True
					self.current = Student()

		elif self.start and tag == "a":
			self.current.setTime(attrs[1][1])

		elif self.start and tag == "img":
			self.current.setImgURL(attrs[0][1])

	def handle_endtag(self, tag):
		if self.start and tag == "div":
			self.start = False
			self.students.stuAdd(self.current)

	def handle_data(self, data):
		if self.start:
			data = data.split(' ',1)
			self.current.setName(data[1].title())
			self.current.setRollno(data[0].upper())

def main():
	os.system('clear')
	login = Login()
	cntin = "Y"
	retSource = RetrieveHTML()
	retSource.login(login)

	while(cntin == "Y" or cntin == "y"):
		os.system('clear')
		print "Fetching Data...Please Wait\n"

		onlineStudents = StudentList()
		parser = LMSDataScraper(onlineStudents)

		retSource.retrieveHTML()
		parser.feed(retSource.getHTML())

		onlineStudents.printData()

		cntin = raw_input("\nRefresh page (y/n): ")

if __name__ == "__main__":
	main()
