import smtplib,ssl
from picamera import PiCamera
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from gpiozero import MotionSensor
import time

pir = MotionSensor(4)
camera = PiCamera()
while True:
	pir.wait_for_motion()
print("Motion is Detected")
camera.start_preview(fullscreen = False, window=(1280,20,650,500))
filename = "/home/Pi/Desktop/"+ (time.strftime("%y%b%t %H:%M:%S"))
camera.capture(filename)     # image path set
pir.wait_for_no_motion()
sleep(5)
camera.stop_preview()


def send_an_emailalert():
	toaddr = 'xyz@gmail.com'  # To emailid PLease change to valid mail id's
	me = 'abc@gmail.com'  # your emailid
	subject = "Motion is detected in Pi Camera"  # Subject

	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = me
	msg['To'] = toaddr
	msg.preamble = "test "

	part = MIMEBase('application', "octet-stream")
	part.set_payload(open(filename, "rb").read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; image= filename')  # File name and format name
	msg.attach(part)

	try:
		s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login(user='adiammu99 @ gmail.com', password = ' ** ** ** ** *')  # User id & password

		s.sendmail(me, toaddr, msg.as_string())
		s.quit()

	except Exception as e:
		print(e)

	send_an_emailalert()


