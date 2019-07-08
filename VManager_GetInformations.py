#!/usr/bin/python
'''
First application ... it`s not already defined
I need to define the application of this file and how to implement it 
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




#============================ helpers =========================================






#============================ main ============================================

try:
    # print banner
    print '\nVMgr_LatencyMote (c) Dust Networks'
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
    macAddress = json.loads(mote_list)
    
    print macAddress

    print mote_list[1]

    # Get the mote Information
    for mote in mote_list.motes:
        mote_info = voyager.motesApi.get_mote_info('00-17-0D-00-00-31-CA-03')
    print mote_info 

except:
    traceback.print_exc()
    print ('Script ended with an error.')
    sys.exit()
