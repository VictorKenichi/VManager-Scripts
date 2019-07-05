#!/usr/bin/python
'''
This script ...

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

count = 0
macAddress = []
life_time = []

#============================ helpers =========================================

def process_data(mydata):
    '''Process data notifications
    Checks whether the notification came from the desired MAC address, 
    then prints latency data and calculates average and max latencies.
    '''
    global count, macAddress, life_time
    
    mycharge = mydata.charge
    myvoltage = mydata.voltage
    if mydata.mac_address in macAddress:
        pass
    else:
        macAddress.append("mydata.mac_address")
    print(len(macAddress))
    rate = myvoltage/mycharge #Verificar esse calculo
    count += 1
    life = []
    life.append("rate")
    print('Mote {0} --> Charge Consumed {1} mC -- Voltage {2} -- Rate {3} -- Count {4} \n'.format(mydata.mac_address, mycharge, myvoltage, rate, count))

def process_notif(notif):
    '''
    Dispatch notifications to specific processing functions
    '''
    if   notif.type in (
            'dataPacketReceived',
            'ipPacketReceived',
        ):
        # handle data notifications
        pass

    elif notif.type in (
            'deviceHealthReport'
        ):
        # handle health reports
        process_data(notif)

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

    # Start listening for data notifications
    voyager.get_notifications(notif_callback=process_notif)

    print '\n==== Subscribing to data notifications'
    reply = raw_input ('\n Waiting for notifications from mote, Press any key to stop\n')

    voyager.stop_notifications()
    print 'Script ended normally'
 
except:
    traceback.print_exc()
    print ('Script ended with an error.')
    sys.exit()
