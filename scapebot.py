' scapebot is a part of Carl Sagans Laboratories '
' authored by Artur Sapek '

from BeautifulSoup import BeautifulSoup
from mechanize import Browser
import urllib2

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

class scapebot():

	def command(self):    # Right now this only searches Comet Tavern
		userinput = raw_input('> ')
		self.Comet_Tavern(userinput)
	
	def Comet_Tavern(self, date):
		br = Browser()
		br.open('http://www.comettavern.com/shows.php')
		br.select_form(nr=0)
		month = months[int(date[0:2]) - 1]
		day = ' %s ' % date[2:4]
		br['month'] = [month]
		results = br.submit(name='submit').read()
		soup = BeautifulSoup(results)
		show = []
		found = False
		for main in soup(id='main'):
			for link in main('a'):
				if day in str(link.renderContents()):
					try:
						entry = br.follow_link(text=link.renderContents(), nr=0).read()
						found = True
					except:
						break
		if found == False:	
			show = 'No show on that day'
		else:
			bands = []
			entry = BeautifulSoup(entry)
			for main in entry(id='main'):
				for band in main('li'):
					bandname = band.renderContents()
					for a in band('a'):
						bandname = a.renderContents()
					bands.append(bandname)
			for extrainfo in entry('center'):
				for font in extrainfo('font'):
					for b in font('b'):
						if '$' in b.renderContents():
							extra = b.renderContents()
							time = extra[0 : extra.index(' ')]
							price = extra[extra.index('$') : len(extra)]
			show.append(bands)
			show.append('%s %s' % (month, day[0:3]))
			show.append(time)
			show.append(price)
		print show
		self.command()


	def email(self, To, Subject, Body):    # For emailing critical errors / progress reports
	
		import smtplib
		from email.MIMEMultipart import MIMEMultipart
		from email.MIMEText import MIMEText
		from email.MIMEBase import MIMEBase
		from email.Utils import COMMASPACE, formatdate
		To = [To]
		assert type(To) == list
		Msg = MIMEMultipart()
		Msg['From'] ='Scapebot'
		Msg['To'] = COMMASPACE.join(To)
		Msg['Subject'] = Subject
		Msg.attach(MIMEText(Body))

		server = smtplib.SMTP('smtp.gmail.com', '587')
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login('artur.sapek', 'chaney15adick')
		server.sendmail('Scapebot', To, Msg.as_string())
		server.quit()

