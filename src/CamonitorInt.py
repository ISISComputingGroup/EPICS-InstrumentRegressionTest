'''
Simple check for specific test, it can be altered and extended as appropriate in the future
'''

from epics import *
import unittest
import time

class keeptrack:
    list=[]
    def moni(self, data):
        self.list.append(data)

def monitored(string):
    global monitoring
    monitoring.moni(string)

def Camonitor_Int(test,**kwargs):
    global monitoring
    PVLIST = kwargs['pvnames']
    pvname = PVLIST[kwargs['pvstouse']]
    monitoring = keeptrack()
    camonitor(pvname,monitored)
    time.sleep(5)
    test.assertTrue(len(monitoring.list) > 0, 'No monitor values were detected on %s' % pvname)
