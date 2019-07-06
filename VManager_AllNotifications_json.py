#!/usr/bin/python
# -*- coding: cp1252 -*-
'''
This script takes all notifications from motes and network...

'''

#============================ adjust path =====================================

import sys
import os
if __name__ == "__main__":
    here = sys.path[0]
    sys.path.insert(0, os.path.join(here, '..', 'libs'))
    sys.path.insert(0, os.path.join(here, '..', 'external_libs'))

#============================ imports =========================================

import urllib3
import traceback
import base64
import certifi
import json

# generic SmartMeshSDK imports
from SmartMeshSDK                      import sdk_version
# VManager-specific imports
from VManagerSDK.vmanager              import Configuration
from VManagerSDK.vmgrapi               import VManagerApi
from VManagerSDK.vmanager.rest         import ApiException
from VManagerSDK.vmanager              import SystemWriteConfig

#============================ defines =========================================

DFLT_VMGR_HOST           = "128.93.102.105"

urllib3.disable_warnings() # disable warnings that show up about self-signed certificates

#============================ variables =======================================
line_counter = 1

#============================ helpers =========================================
def process_dataPacketReceived(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter
        
    print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
    line_counter += 1

    data = {
        mydata.type: {
            "Latency": mydata.latency,
            "macAddress": mydata.mac_address
            }
        }
    json.dump(data, file)

def process_apStateChanged(mydata):
    '''Process data notifications from dataPacketReceived'''
    global line_counter
        
    print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
    line_counter += 1

    data = {
        mydata.type: {
            "state": mydata.state,
            "type": mydata.type
            }
        }
    json.dump(data, file)
    
def process_deviceHealthReport(mydata):
    '''Process data notifications from HealthReport'''
    global line_counter
        
    print 'Writting Line {0} -- Data Notification : {1}\n'.format(line_counter, mydata.type)
    line_counter += 1

    data = {
        mydata.type: {
            "type": mydata.type,
            "sysTime": mydata.sysTime,
            "macAddress": mydata.mac_address,
            "temperature (Celsius)": mydata.temperature,
            "charge (mC)": mydata.charge,
            "voltage (mV)": mydata.voltage
            }
        }
    #json.dumps(data, indent=4)
    json.dump(data, file, indent=4)
    
def process_notif(notif):
    '''
    Dispatch notifications to specific processing functions
    '''
    if   notif.type in (
            'dataPacketReceived',
            'ipPacketReceived',
        ):
        # handle data notifications
        process_dataPacketReceived(notif)
        
    
    elif notif.type in (
            'deviceHealthReport'
        ):
        # handle health reports
        process_deviceHealthReport(notif)

    elif notif.type in (
            'apStateChanged'
        ):
        # handle apStateChanged reports
        process_apStateChanged(notif)
        
    elif notif.type in (
            'configChanged', 
            'configDeleted', 
            'configLoaded', 
            'configRestored',
        ):
        # handle config notifications
        pass
    

    else:
        # handle other event notifications
        pass

#============================ main ============================================

try:
    # print banner
    print '\nVMgr_LifeTime (c) Dust Networks'
    print 'SmartMesh SDK {0}\n'.format('.'.join([str(i) for i in sdk_version.VERSION]))

    # ask the user for VManager host
    mgrhost = raw_input('Enter the IP address of the manager (e.g. {0} ): '.format(DFLT_VMGR_HOST))
    if mgrhost == "":
        mgrhost = DFLT_VMGR_HOST

    # log-in as user "dust"
    config = Configuration()
    config.username     = 'dust'
    config.password     = 'dust'
    config.verify_ssl   = False
    
    if os.path.isfile(certifi.where()):
        config.ssl_ca_cert  = certifi.where()
    else:
        config.ssl_ca_cert = os.path.join(os.path.dirname(sys.executable), "cacert.pem")

    # initialize the VManager Python library
    voyager = VManagerApi(host=mgrhost)

    # Get the whole list of motes 
    mote_list = voyager.motesApi.get_motes()

    # Get Mote Info
    # mote_info = voyager.motesApi.get_mote_info()

    # for mote in mote_list.motes:
    #   print mote.mac_address

    file = open("json_test.json","w")
    #with open(os.path.join('C:\INRIA-Victor\VManager\Scripts\smartmeshsdk\VManager Data',"teste.txt"), "w") as file:
    print 'Script Created Successfully !'

    # Start listening for data notifications
    voyager.get_notifications(notif_callback=process_notif)

    print '\n==== Subscribing to data notifications'
    reply = raw_input ('\n Waiting for notifications from mote, Press any key to stop\n')

    file.close
    print 'Script Closed'
    
    voyager.stop_notifications()
    print 'Script ended normally'
 
except:
    traceback.print_exc()
    print ('Script ended with an error.')
    sys.exit()
