#!/usr/bin/python3
#
# Simple python script for detecting the doorbell
#
# Version 0.7 - march 2020 Ray-Hoo
#
#################################################

import RPi.GPIO as GPIO
import datetime
import time
import smtplib

# Setting the GPIO mode and previous state of the doorbell
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.IN)
previous=GPIO.input(15)

# Mail routine
def doormail( curdat ):
  from email.message import EmailMessage

  msg = EmailMessage()
  msg.set_content('There is someone at the door @ {}.'.format(curdat))

  fromEmail = 'fromwho@mailaddress.com'
  toEmail = 'towho@mailaddress.com'

  msg['Subject'] = 'There is someone at the door @ {}'.format(curdat)
  msg['From'] = fromEmail
  msg['To'] = toEmail

  s = smtplib.SMTP('IP-address', 25)
  s.send_message(msg)
  s.quit()

# Loop to have a continous checking of the doorbell
while True:
  current=GPIO.input(15) 
  if current:
    if current!=previous:
       curdat=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")
       print("{} - Doorbell has been pressed".format(curdat))
       doormail ( curdat )
       previous=current
  else:  
    if current!=previous:
       curdat=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")
       print("{} - Doorbell has been released".format(curdat))
       time.sleep(10) # To prevent multiple mails when doorbell is pressed multiple times in a short period.
       previous=current
