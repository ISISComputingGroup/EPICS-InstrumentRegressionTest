'''
The umberella code to deal with the TEST xml and call the build test code as appropriate
'''

from __future__ import print_function
from epics import PV
from CagetDatim import Caget_Datim
from CaputZero import Caput_Zero
from CamonitorInt import Camonitor_Int
from GenerateLog import GenerateLog
from PrintInfo import *
import unittest
import xml.etree.ElementTree as etree
import os

#instrument_test is the main test code
def instrument_test(kwargs):
    #Set the default directory to the local directory for the file - this may need to change
    dir = os.path.dirname(__file__)
    #If a specific set of 'tests' has been specified use that file, otherwise use the default one
    try:
        test_desc = kwargs['tests']
    except:
        test_desc = os.path.join(dir,'TEST.xml')
    #Set the debug variable to a value passed in, or default to not debugging
    try:
        debug = kwargs['debug']
    except:
        debug = 0
    set_debug(debug)
    #Set the gen_log variable to a value passed in, or default to logging
    try:
        gen_log = kwargs['gen_log']
    except:
        gen_log = 1
    
    #Get the items from an XML document rather than hard code them here
    try:
        tree = etree.parse(test_desc)
    except:
        return 'No tests found'
    testdir = tree.findtext('test_directory')
    if testdir == None:
        testdir = os.path.join(os.environ['ICPVARDIR'],'logs/testlog')
	print('testdir = %s'%testdir)
    #Set a delay variable, hopefully this will allow for creating an unstable test environment at times
    node = tree.find('delay')
    try:
        delay = int(node.text)
    except:
        delay = 2
    
    #Generate a dictionary of the tests from the XML
    TESTS = {}
    test = tree.find('TESTS')
    if test == None:
        return 'No TESTS found'
    node = test.findall('TEST')
    testnum = 1
    for x in node:
        pvs = {}
        ttype = x.findtext('test-type')
        if ttype == None:
            ttype = 'Unknown'
        expval = x.findtext('expval')
        scope = x.findtext('scope')
        if scope == None:
            scope = 'Unknown'
        format = x.findtext('data-format')
        dtype = x.findtext('data-type')
        pvstouse = x.findtext('pvstouse')
        for pv in x.findall('pv'):
            pvs[pv.attrib['pvnum']]=pv.text
        TESTS[testnum] = (ttype,expval,scope,format,dtype,pvstouse,pvs)
        testnum = testnum + 1
    
    #Set up the test log file
    log_file = 'test_log.txt'
    logf = open(log_file, 'w')
    runner = unittest.TextTestRunner(logf, verbosity=1)
    
    #Class for the simplification of PV creation
    class pvrec:
        pvinst = ''
        val = ''
        
        def initpv(self, pvname):
            pvrec.pvinst = PV(pvname)
           
    #Set up the testing suite
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    #Set up the PVs to use, and create the dictionary for later use
    actualpvs = {}
    
    #Get the PV names used from the test cases entered
    allpv_names = []
    for x,TEST in TESTS.iteritems():
        pvstouse = ('%s'%TEST[5])
        pvslist = pvstouse.split(',')
        all_pvs = TEST[6]
        for i in pvslist:
            pvname = all_pvs[i]
            testing = pvrec()
            testing.initpv(pvname)
            actualpvs[('%s,%s'%(x,i))] = testing.pvinst
        pvsintest = len(pvslist)
        updatedtest=list(TEST)
        updatedtest.append(pvsintest)
        TEST=tuple(updatedtest)
        TESTS[x]=TEST
    
    testdets = {}
    #Generate and run the tests
    for x,TEST in TESTS.iteritems():
        ttype = TEST[0]
        expval = TEST[1]
        scope = TEST[2]
        format = TEST[3]
        dtype = TEST[4]
        pvstouse = TEST[5]
        pvnames = TEST[6]
        pvsinlist = TEST[7]
        curr_test = 'Test %s: Type = %s, scope = %s'%(x,ttype,scope)
        print_info('Currently building %s\n' % curr_test)
        testdets[x] = curr_test
        logf.write(('Test %s: %s\n'%(x,TEST)))
        class IterationTests(unittest.TestCase):
            if ttype == 'Unknown':
                def test_unkown(self):
                    self.assertTrue(False, 'Unknown Test not actioned')
            if ttype =='Caget-Datim':
                def test_caget_datim(self):
                    Caget_Datim(self,x=x,pvstouse=pvstouse,actualpvs=actualpvs,format=format,expval=expval,pvsinlist=pvsinlist)
            if ttype =='Caput-Zero':
                def test_caput_zero(self):
                    Caput_Zero(self,x=x,pvstouse=pvstouse,actualpvs=actualpvs,expval=expval,delay=delay)
            if ttype =='Camonitor-Int':
                def test_camonitor_int(self):
                    Camonitor_Int(self,pvstouse=pvstouse,pvnames=pvnames)
        itersuite = unittest.TestLoader().loadTestsFromTestCase(IterationTests)
        print_info('Running Test...\n')
        runner.run(itersuite)
        
    logf.close()
    
    print_info('Tests Complete.')
    if gen_log == 1:
        print_info('Generating Log File.')
    pass_state = GenerateLog(testdir,log_file,TESTS,testdets,gen_log)
    return pass_state

#inst_test is for use as an external command to allow for the _msgs version to add a kwarg
def inst_test(**kwargs):
    return instrument_test(kwargs)

#inst_test_msgs is an external command which forces the addition of debug = 1 so that info is displayed
def inst_test_msgs(**kwargs):
    kwargs['debug']=1
    return instrument_test(kwargs)

#main here so that the system can be tested in debug mode (or not if code is altered) and outcome is displayed
def main():
    pass_state = inst_test(debug = 1)
    print('Pass State = %s'%pass_state)
    
if __name__ == '__main__':
    main()