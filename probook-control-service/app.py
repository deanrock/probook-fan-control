#!/usr/bin/python
import socket
from threading import Thread
import os
import subprocess
from time import sleep

def getTemperature():
	temp = subprocess.Popen("sensors | grep Physical | cut -b 18-19", stdout=subprocess.PIPE, shell=True).stdout.read()

	return temp.strip()

def send(cmd):
	s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
	s.sendto(cmd, "/tmp/probook-socket")

while 1:
	temp=int(getTemperature())

	print temp

	speed = 0x80

	if temp > 95:
		speed = 0x00
	elif temp > 90:
		speed = 0x19
	elif temp > 85:
		speed = 0x29
	elif temp > 80:
		speed = 0x39
	elif temp > 75:
		speed = 0x49
	elif temp > 70:
		speed = 0x59
	elif temp > 65:
		speed = 0x70
	elif temp > 60:
		speed = 0x80
	else:
		speed = 0xFF


	if speed == 0xFF:
		send("fanoff")
	else:
		send("setfan 0x%x" %(speed))
		print "setfan 0x%x" %(speed)
	sleep(1)