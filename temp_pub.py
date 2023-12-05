from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import os
import glob
import time
import datetime

# Initialize the GPIO Pins
os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm') # Turns on the Temperature module

# Finds the correct device file that holds the temperature data
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# A function that reads the sensors data
def read_temp_raw():
  f = open(device_file, 'r') # Opens the temperature device file
  lines = f.readlines() # Returns the text
  f.close()
  return lines

# Convert the value of the sensor into a temperature
def read_temp():
  lines = read_temp_raw() # Read the temperature 'device file'

  # While the first line does not contain 'YES', wait for 0.2s
  # and then read the device file again.
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_temp_raw()

  # Look for the position of the '=' in the second line of the
  # device file.
  equals_pos = lines[1].find('t=')

  # If the '=' is found, convert the rest of the line after the
  # '=' into degrees Celsius, then degrees Fahrenheit
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    return temp_c

# Messaging setup
host = "xxxxxxxxxxxx-ats.iot.eu-west-1.amazonaws.com"		# this should be the address of your hostname at AWS
certPath = "/home/jonas/aws_temp/RPi3_policy/"	        # wherever your certificates are located

clientId = "RPi3_B"				                              # your AWS IoT device name
sensorType = "temperature"                              # 
query = "pub"
area = "grondal"

topic = area+"/"+clientId+"/"+sensorType+"/"+query		# the name of the topic your messages will be written to
print(topic)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)

myAWSIoTMQTTClient.configureCredentials(
	"{}AmazonRootCA1.pem".format(certPath), 
	"{}5d08ef7/.../28179-private.pem.key".format(certPath),
	"{}5d08ef7/.../8a8f2d1ee8928179-certificate.pem.crt".format(certPath))


# AWSIoTMQTTClient connection configuration

myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)

myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myAWSIoTMQTTClient.connect()

# Publish to the same topic in a loop forever

#while True: Loop excluded when running on cronjob
message = {}
message['timestamp'] = str(datetime.datetime.now())
message['temperature'] = read_temp()
messageJson = json.dumps(message)
myAWSIoTMQTTClient.publish(topic, messageJson, 1)
print('Published topic %s: %s\n' % (topic, messageJson))

#time.sleep(5)					# Sleep 10 seconds between loops
myAWSIoTMQTTClient.disconnect()
