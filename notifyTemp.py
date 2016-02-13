#!/usr/bin/env python

import os
import time
import datetime
import glob
from time import strftime
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor = '/sys/bus/w1/devices/28-0215658c80ff/w1_slave'
 
def tempRead():
        t = open(temp_sensor, 'r')
        lines = t.readlines()
        t.close()
 
        temp_output = lines[1].find('t=')
        if temp_output != -1:
                temp_string = lines[1].strip()[temp_output+2:]
                temp_c = (float(temp_string)/1000.0*9/5+32)
        return round(temp_c,1)
 
while True:
    temp = tempRead()
    print temp
    datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
    print datetimeWrite
    break

now = datetime.datetime.now().strftime('%H:%M')

#verify if the sensor is working
if temp == None:
  msg = MIMEMultipart()
  msg['From'] = 'XXXX@gmail.com'
  msg['To'] = 'XXXX@txt.att.net'
  msg['Subject'] = 'Sensor problem' 
  message = ("The f'ing sensor isn't working")
  msg.attach(MIMEText(message))
  mailserver = smtplib.SMTP('smtp.gmail.com', 587)
  mailserver.ehlo()
  mailserver.starttls()
  mailserver.ehlo()
  mailserver.login('xxx@gmail.com', 'mypassword')
  mailserver.sendmail('xxx@gmail.com', 'xxx@gmail.com', msg.as_string())
  mailserver.quit()
  
#send text msg if temperature < 55
if temp <= 55:
  msg = MIMEMultipart()
  msg['From'] = 'XXXX@gmail.com'
  msg['To'] = 'XXXX@txt.att.net'
  msg['Subject'] = 'Temperature too low !'
  message = ("Temperature is under 55°f. It's {}.The temperature is {}°f".format(now,ds18b20Temp))
  msg.attach(MIMEText(message))
  mailserver = smtplib.SMTP('smtp.gmail.com', 587)
  mailserver.ehlo()
  mailserver.starttls()
  mailserver.ehlo()
  mailserver.login('xxx@gmail.com', 'mypassword')
  mailserver.sendmail('xxx@gmail.com', 'xxx@gmail.com', msg.as_string())
  mailserver.quit()
