#!/usr/bin/env python3

##############################################################################
# Dump data from Tesla Powerwall
##############################################################################
# Simon Moore, Nov 2019
##############################################################################
# Notes:
#  - Unofficial documentation:
#      https://github.com/vloschiavo/powerwall2
#  - To get access, you may need to login (e.g. via a browser) as a customer
#    - Forum posts suggest using an empty username and "S"+device serial number as the password
#  - my URL to the gateway: https://192.168.1.201/

import json
import requests
import datetime
import time
import logging
# inhibit warnings about insecure https access
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

##############################################################################
# CHANGE THE FOLLOWING PARAMETERS TO SUIT YOUR SETUP
##############################################################################
# IP address of your PowerWall:
powerwallip = "192.168.1.60"
# What directory do you want your log files to be written to?
logfilebase = "/home/swm11/homeautomation/powerwall/logs/teslalog"

def dumpPowerwall(logfile,now):
    # get agrigated meter readings
    response = requests.get("https://"+powerwallip+"/api/meters/aggregates",verify=False)
    d = json.loads(response.text)

    # get fault information
    response = requests.get("https://"+powerwallip+"/api/system_status/grid_faults",verify=False)
    faults = response.text

    # get battery charge level
    response = requests.get("https://"+powerwallip+"/api/system_status/soe",verify=False)
    energy = json.loads(response.text)

    # create a dict holding site info
    x = {"time"  : now.isoformat(),
         "last_communication_time" : d["site"]["last_communication_time"],
         "battery_charge_pc" : energy["percentage"],
         "faults" : faults}
    for meter in ["site","load","battery","solar"]:
        x[meter] = { "energy_exported" : d[meter]["energy_exported"],
                     "energy_imported" : d[meter]["energy_imported"] }
    json.dump(x,logfile)
    logfile.write("\n")


# Simple loop that checks the time every second and dumps data every five
# minutes.  Creates a log file for each day. 
while True:
    now = datetime.datetime.now()
    fn = "teslalog-%04d%02d%02d.json" % (now.year,now.month,now.day)
    day = now.day
    while (now.day == day):
        with open(fn,'a') as logfile:
            cnt = 0;
            while((cnt<25) and (cnt>=0)):
                try:
                    dumpPowerwall(logfile,now)
                except:
                    time.sleep(2)
                    cnt = cnt+1
                else:
                    # print("Dumping at "+now.isoformat())
                    cnt = -1
            logfile.close()
            if(cnt>0):
                logging.error("Failed to run dumpPowerwall() after "+str(cnt)+" retries")

        nextmin = (int(now.minute/5)*5+5) % 60
        # nextmin = (now.minute+1) % 60
        while now.minute != nextmin:
            time.sleep(1)
            now = datetime.datetime.now()
        

exit(0)




