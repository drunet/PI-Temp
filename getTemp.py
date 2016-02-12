#!/usr/bin/python

import pigpio
import time
import os
import sys
import datetime
import subprocess
import smbus
import random
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
sys.path.append("/usr/local/bin/")

DS18B20_SERIAL_NUMBER="28-xxxxxxxxxx"

def readDS18B20(sensorId):
   if sensorId == None:
     return None
   retry=0
   while(1):
     try:
       filer = open( "/sys/bus/w1/devices/" + sensorId + "/w1_slave")
       text1 = filer.read()
       filer.close()
       line1 = text1.split("\n")[0]
       crc = line1.split("crc=")[1]
       if crc.find("YES")>=0:
        break;
     except:
        #ok error, loop it 
        pass

     retry = retry + 1
     if retry >= 5 :
       return None
    
   #ok Valid temperature
   line2 = text1.split("\n")[1]
   text2 = line2.split(" ")[9]
   return (float((text2[2:])/1000.0)*9/5+32)

#read sensor again but now keep the data
ds18b20Temp = readDS18B20(DS18B20_SERIAL_NUMBER)
if ds18b20Temp != None:
   ds18b20Temp = round(ds18b20Temp * 2.0 ,0)/2

now = datetime.datetime.now().strftime('%H:%M')

#verify if the sensor is working
if ds18b20Temp == None:
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
  
#send mail if temperature < 55
if ds18b20Temp <= 55:
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
