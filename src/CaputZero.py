'''
Simple check for specific test, it can be altered and extended as appropriate in the future
'''

import time


def Caput_Zero(test,**kwargs):
    PVLIST = kwargs['actualpvs']
    pvid = '%s,%s'%(kwargs['x'],kwargs['pvstouse'])
    pv = PVLIST[pvid]
    pv.put(unichr(0))
    time.sleep(kwargs['delay'])
    pvval = pv.get()
    test.assertEqual(('%s'%pvval), kwargs['expval'], ('%s response to %s is not equal to %s' % (pvval,pv,kwargs['expval'])))
