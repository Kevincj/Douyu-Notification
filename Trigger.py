import time
import datetime
import requests
import smtplib
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class LogProcessor():
	def __init__(self):
		self.fileName = 'trigger.log'

	def CreateLogFile(self):
		print 'Creating log file...'
		with open(self.fileName, 'w') as f:
			f.write('Created log file.\n')
			f.close()
			return True
		return False

	def GetCurrentTimeForLogger(self):
		timestamp = time.time()
		return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

	def Log(self, str):
		with open(self.fileName, 'a+') as f:
			f.write(str+'\n')
			f.close()

class DouyuRoomNotification():
	def __init__(self, logger):
		print 'Reading json file...'
		data = self.ReadData()
		self.email = data['email']
		self.password = data['password']
		self.room_id = data['room_id']
		print 'Success.'

		self.logger = logger

		self.url = "http://open.douyucdn.cn/api/RoomApi/room/" + self.room_id
		self.room_status = None

	def ReadData(self):
		with open('data.json') as f:
			return json.load(f)

	def Run(self):
		while not self.logger.CreateLogFile():
			time.sleep(0.1)
		print 'Success.'

		self.room_status = self.InitRoomStatus()
		print 'Success.'

		while True:
			CheckStatus(self.room_status)

	def InitRoomStatus(self):
		print 'Start init room_status...'
		while True:
			try:
				print self.url
				r = requests.get(url=self.url)
				print r
				data = r.json()
				self.logger.Log('Start as ' + self.GetStringForCode(data[u'data'][u'room_status']))
				return self.GetStatusForCode(data[u'data'][u'room_status'])
			except Exception as e:
				self.logger.Log('Exception caught, retry in 1 sec...')
				time.sleep(1)

	def GetCodeForStatus(self):
		return u'1' if self.room_status else u'2'

	def GetStringForStatus(self):
		return 'Online' if self.room_status else 'Offline'

	def GetStringForCode(self, code):
		return 'Online' if code == u'1' else 'Offline'

	def GetStatusForCode(self, code):
		return True if code == u'1' else 'False'

	def CheckStatus(self):
		while True:
			standard_time = self.logger.GetCurrentTimeForLogger()
			try:
				r = requests.get(url=self.url)
				data = r.json()
				if data[u'data'][u'room_status'] != self.GetCodeForStatus():
					self.room_status = not self.room_status
					self.TriggerIFTTT()
					self.logger.Log(self.GetStringForStatus() + "!")
					break
				else:
					self.logger.Log(self.GetStringForStatus() + ' at ' + standard_time)
					time.sleep(60)
			except Exception as e:
				self.logger.Log('Exception caught, retry in 1 sec...')
				time.sleep(1)


	def TriggerIFTTT(self):
		tag = '#' + self.GetStringForStatus()

		message = 'Notification'
		msg = MIMEMultipart()
		msg['From'] = self.email
		msg['To'] = 'trigger@applet.ifttt.com'
		msg['Subject'] = tag
		msg.attach(MIMEText(message, 'plain'))

		server = smtplib.SMTP(host='smtp.gmail.com',port=587)
		server.starttls()
		server.login(self.email, self.password)

		server.sendmail(msg['From'], msg['To'], msg.as_string())
		server.quit()

		self.logger.Log('Sent a trigger : ' + tag)



if __name__ == '__main__':
	notification = DouyuRoomNotification(LogProcessor())
	notification.Run()

