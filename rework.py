#!/usr/bin/env python

import os
import time
import urllib

from restStuff import *

cardIp = "169.254.0.1"
# This is the APIPA Address, this one can be changed but considering this is the best way to configure the script


# update the password to allow ssh access // Password tempPasswd@3.0.5 can be changed as the password you need
os.environ["BIOS_URL"] = "https://" + cardIp + "/rest/mbdetnrs/1.0"

restClient = BiosClient()
print (restClient.changePassword("admin", "admin", "tempPasswd@3.0.5"))

exit(0)
