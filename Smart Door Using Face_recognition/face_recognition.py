import RPi.GPIO as GPIO
import time
import picamera
import smtplib
import face_recognition
from time import sleep

from email.mime.multipart import MIMEMultipart
#from email.MIMEText import MIMEText
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
 
fromaddr = "smartdoorgmrit789@gmail.com"    # change the email address accordingly
toaddr = "vamsikrishnapapana@gmail.com"
 
mail = MIMEMultipart()
 
mail['From'] = fromaddr
mail['To'] = toaddr
mail['Subject'] = "Attachment"
body = "Please find the attachment"

class Motor(object):
    def __init__(self, pins):
        self.P1 = pins[0]
        self.P2 = pins[1]
        self.P3 = pins[2]
        self.P4 = pins[3]
        self.deg_per_step = 360.0 / 512  # for half-step drive (mode 3)
        print(self.deg_per_step)
        self.steps_per_rev = 512  # 4096
        self.step_angle = 0  # Assume the way it is pointing is zero degrees
        print(self.deg_per_step, self.steps_per_rev, self.step_angle)
        self._T = 0.005
        for p in pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, 0)
            
    def move_to(self, angle):
        """Take the shortest route to a particular angle (degrees)."""
        # Make sure there is a 1:1 mapping between angle and stepper angle
        target_step_angle = int(angle / self.deg_per_step)
        steps = target_step_angle - self.step_angle
        steps = (steps % self.steps_per_rev)
        print(self.deg_per_step, target_step_angle, self.step_angle, steps)
        if steps > self.steps_per_rev / 2:
            steps -= self.steps_per_rev
            self._move_acw(-steps)
        else:
            self._move_cw(steps)
        self.step_angle = target_step_angle

    def __clear(self):
        GPIO.output(self.P1, 0)
        GPIO.output(self.P2, 0)
        GPIO.output(self.P3, 0)
        GPIO.output(self.P4, 0)

    def _move_acw(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            #print(i)
            GPIO.output(self.P3, 0)
            GPIO.output(self.P1, 1)
            sleep(self._T * 2)
            GPIO.output(self.P2, 0)
            GPIO.output(self.P4, 1)
            sleep(self._T * 2)
            GPIO.output(self.P1, 0)
            GPIO.output(self.P3, 1)
            sleep(self._T * 2)
            GPIO.output(self.P4, 0)
            GPIO.output(self.P2, 1)
            sleep(self._T * 2)

    def _move_cw(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            GPIO.output(self.P4, 0)
            GPIO.output(self.P2, 1)
            sleep(self._T * 2)
            GPIO.output(self.P1, 0)
            GPIO.output(self.P3, 1)
            sleep(self._T * 2)
            GPIO.output(self.P2, 0)
            GPIO.output(self.P4, 1)
            sleep(self._T * 2)
            GPIO.output(self.P3, 0)
            GPIO.output(self.P1, 1)
            sleep(self._T * 2)


def sendMail(data):
    mail.attach(MIMEText(body, 'plain'))
    dat='%s.jpg'%data
    print (dat)
    attachment = open(dat, 'rb')
    image=MIMEImage(attachment.read())
    attachment.close()
    mail.attach(image)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "project@123")
    text = mail.as_string()
    print("Processing Image")
    known_image = face_recognition.load_image_file("/home/pi/Documents/vamsi.jpeg")
    unknown_image = face_recognition.load_image_file("/home/pi/Documents/img.jpg")
    biden_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
    if results[0]==True:
        print("Welcome Home")
        GPIO.setmode(GPIO.BOARD)
        m = Motor([11,13,15,16])
        m.move_to(-90)
        sleep(1)
        m.move_to(0)
        sleep(1)
    else:
        print("Intruder...")
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

def capture_image():
    data="img"
    camera.start_preview()
    time.sleep(5)
    camera.capture('%s.jpg'%data)
    camera.stop_preview()
    time.sleep(1)
    sendMail(data)
    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

GPIO.output(3, 0)
camera = picamera.PiCamera()
camera.rotation=0
camera.awb_mode= 'auto'
camera.brightness=50
while True:
  i=GPIO.input(18)
  print(i)
  if i==1:                 #When output from motion sensor is LOW
     print ("Motion Detected")
     GPIO.output(3, 1)
     capture_image()
     time.sleep(1)
        
    #Turn OFF LED
#     time.sleep(0.1)
  elif i==0:               #When output from motion sensor is HIGH
      print ("No Motion detected")
      GPIO.output(3, 0)
      time.sleep(0.01)#Turn ON LED
#      time.sleep(0.1)