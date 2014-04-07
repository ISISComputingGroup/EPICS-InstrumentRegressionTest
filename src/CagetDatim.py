from epics import PV
import unittest
import time

def Caget_Datim(test,**kwargs):
    PVLIST = kwargs['actualpvs']
    if kwargs['pvsinlist'] == 1:
        pvid = '%s,%s'%(kwargs['x'],kwargs['pvstouse'])
        pv = PVLIST[pvid]
        pvval = pv.get()
        timeval = time.strptime(pvval, kwargs['format'])
        testval = time.strftime('%m/%d/%Y %H:%M',timeval)#remove seconds for time lag
        if kwargs['expval'] == 'TOD':
            expected = time.strftime('%m/%d/%Y %H:%M', time.localtime())#today's date time
        else:
            expected = kwargs['expval']
        test.assertEqual(testval, expected, ('%s response to %s is not equal to %s' % (pvval,pv,expected)))