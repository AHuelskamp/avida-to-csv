"""
Logger to be used for avida to json converter 

For more documentation visit: 
https://docs.python.org/3/library/logging.html
"""

import logging 

#format of messages to be sent to logger. 
FORMAT='%(asctime)-15s %(message)s'

#default level of logger for now. 
#this will be set in the argparser at some point later. 
LEVEL="DEBUG" 

logging.basicConfig(format=FORMAT,level=LEVEL)

logging.info('Info')
logging.warning('Warning stuff') 
